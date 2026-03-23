# -*- coding: utf_8 -*-
"""Helpers for Android deeplink inventory probing."""

from datetime import datetime, UTC
import logging
import re

from mobsf.StaticAnalyzer.models import StaticAnalyzerAndroid
from mobsf.MobSF.utils import python_dict

logger = logging.getLogger(__name__)

TOP_ACTIVITY_PATTERNS = (
    re.compile(
        (
            r'mResumedActivity:\s+ActivityRecord\{[^\n]*\s'
            r'(?P<package>[\w.]+)/(?P<activity>[^ }\n]+)'
        ),
    ),
    re.compile(
        (
            r'topResumedActivity=ActivityRecord\{[^\n]*\s'
            r'(?P<package>[\w.]+)/(?P<activity>[^ }\n]+)'
        ),
    ),
    re.compile(
        (
            r'ResumedActivity:\s+ActivityRecord\{[^\n]*\s'
            r'(?P<package>[\w.]+)/(?P<activity>[^ }\n]+)'
        ),
    ),
    re.compile(
        (
            r'mFocusedApp=.*ActivityRecord\{[^\n]*\s'
            r'(?P<package>[\w.]+)/(?P<activity>[^ }\n]+)'
        ),
    ),
)
START_ACTIVITY_PATTERN = re.compile(
    r'(?:Activity:|cmp=)(?P<package>[\w.]+)/(?P<activity>[^ }\n]+)')
MAX_DYNAMIC_PROBE_TARGETS = 64
UNSAFE_ADB_URI_TOKENS = (';', '&&', '||', '$(')


def parse_resumed_activity(output):
    """Parse the foreground activity from dumpsys output."""
    if not output:
        return {}
    for pattern in TOP_ACTIVITY_PATTERNS:
        match = pattern.search(output)
        if match:
            return {
                'package': match.group('package'),
                'activity': match.group('activity'),
            }
    return {}


def get_inventory_from_db(checksum):
    """Fetch deeplink inventory from the static analyzer DB."""
    try:
        static_android_db = StaticAnalyzerAndroid.objects.get(MD5=checksum)
        inventory = python_dict(static_android_db.DEEPLINK_INVENTORY)
        probe_results = python_dict(static_android_db.DEEPLINK_PROBE_RESULTS)
        return static_android_db, inventory, probe_results
    except Exception:
        logger.exception('Unable to fetch deeplink inventory for %s', checksum)
        return None, {}, {}


def get_probe_targets(
        inventory,
        extra_urls=None,
        limit=MAX_DYNAMIC_PROBE_TARGETS):
    """Build a deduped deeplink probe target list."""
    targets = []
    for item in inventory.get('probe_targets', []):
        url = item.get('url')
        if not url or any(token in url for token in UNSAFE_ADB_URI_TOKENS):
            continue
        targets.append({
            'url': url,
            'source': item.get('source', 'inventory'),
            'component': item.get('component', ''),
            'confidence': item.get('confidence', 'low'),
        })
    if extra_urls:
        for url in extra_urls:
            url = (url or '').strip()
            if not url or any(token in url for token in UNSAFE_ADB_URI_TOKENS):
                continue
            targets.append({
                'url': url,
                'source': 'manual',
                'component': '',
                'confidence': 'manual',
            })
    deduped = []
    seen = set()
    for item in targets:
        if item['url'] in seen:
            continue
        seen.add(item['url'])
        deduped.append(item)
    return deduped[:limit]


def run_deeplink_probes(env, package, targets):
    """Run deeplink probes on a connected Android device."""
    results = []
    matched = 0
    errors = 0
    for target in targets:
        url = target['url']
        env.adb_command(['am', 'force-stop', package], True, True)
        am_out = env.adb_command([
            'am',
            'start',
            '-W',
            '-a',
            'android.intent.action.VIEW',
            '-d',
            url,
        ], True, True)
        env.wait(1)
        dump_out = env.adb_command(['dumpsys', 'activity', 'activities'],
                                   True, True)
        am_text = am_out.decode('utf-8', 'ignore') if am_out else ''
        dump_text = dump_out.decode('utf-8', 'ignore') if dump_out else ''
        resumed = parse_resumed_activity(dump_text)
        started = START_ACTIVITY_PATTERN.search(am_text)
        package_match = resumed.get('package') == package
        start_match = started and started.group('package') == package
        matched_activity = resumed.get('activity', '')
        if not matched_activity and started:
            matched_activity = started.group('activity')
        if package_match or start_match:
            status = 'matched'
            matched += 1
        elif 'Error:' in am_text:
            status = 'error'
            errors += 1
        else:
            status = 'miss'
        results.append({
            'url': url,
            'source': target.get('source', 'inventory'),
            'expected_component': target.get('component', ''),
            'confidence': target.get('confidence', 'low'),
            'status': status,
            'matched_package': resumed.get('package', ''),
            'matched_activity': matched_activity,
            'am_output': am_text[:500],
        })
    return {
        'generated_at': datetime.now(UTC).isoformat(),
        'package': package,
        'total': len(results),
        'matched': matched,
        'missed': len(results) - matched - errors,
        'errors': errors,
        'results': results,
    }


def persist_deeplink_probe_results(checksum, report):
    """Persist deeplink probe results back to the static analyzer DB."""
    StaticAnalyzerAndroid.objects.filter(MD5=checksum).update(
        DEEPLINK_PROBE_RESULTS=report)
