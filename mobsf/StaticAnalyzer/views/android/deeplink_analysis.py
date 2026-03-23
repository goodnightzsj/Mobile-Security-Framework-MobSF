# -*- coding: utf_8 -*-
"""Best-effort Android deeplink inventory analysis."""

import logging
import re
from pathlib import Path
from urllib.parse import urlparse

from mobsf.MobSF.utils import (
    append_scan_status,
    get_android_src_dir,
)

logger = logging.getLogger(__name__)

DEEPLINK_LITERAL_REGEX = re.compile(
    r'(?P<uri>(?:intent://|[A-Za-z][A-Za-z0-9+.\-]{1,50}://)[^"\')\s<>]+)')
NAV_DEEPLINK_REGEX = re.compile(r'app:uri\s*=\s*"([^"]+)"')
HANDLER_HINTS = {
    'onNewIntent': 'onNewIntent(',
    'getIntent': 'getIntent(',
    'getData': '.getData(',
    'getDataString': '.getDataString(',
    'getQueryParameter': '.getQueryParameter(',
    'getQueryParameters': '.getQueryParameters(',
    'getScheme': '.getScheme(',
    'getHost': '.getHost(',
    'getPath': '.getPath(',
    'getPathSegments': '.getPathSegments(',
    'intentActionView': 'Intent.ACTION_VIEW',
    'androidActionView': 'android.intent.action.VIEW',
    'navDeepLink': 'navDeepLink(',
}
SCANNED_SOURCE_EXTENSIONS = {'.java', '.kt'}
SCANNED_RESOURCE_EXTENSIONS = {'.xml'}
EXCLUDED_SCHEMES = {'javascript', 'data', 'file'}
MAX_CANDIDATE_URLS = 8
MAX_PROBE_TARGETS = 64
MAX_EVIDENCE_ITEMS = 8


def _strip_scheme_separator(scheme):
    if scheme.endswith('://'):
        return scheme[:-3]
    return scheme


def _dedupe(items):
    seen = set()
    deduped = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _clean_uri(uri):
    return uri.strip().strip('\'"(),;')


def _is_deeplink_uri(uri):
    if not uri:
        return False
    if uri.startswith('intent://'):
        return True
    parsed = urlparse(uri)
    if not parsed.scheme:
        return False
    return parsed.scheme.lower() not in EXCLUDED_SCHEMES


def _component_hints_from_path(relative_path):
    base = relative_path.replace('\\', '/')
    if '.' not in base:
        return set()
    no_ext = base.rsplit('.', 1)[0]
    hints = {no_ext.replace('/', '.')}
    hints.add(no_ext.rsplit('/', 1)[-1])
    return hints


def _component_matches(component, hints):
    if not component or not hints:
        return False
    simple_name = component.rsplit('.', 1)[-1].rsplit('$', 1)[0]
    return component in hints or simple_name in hints


def _resource_dirs(app_dir, typ):
    roots = []
    if typ == 'apk':
        roots.append(app_dir / 'apktool_out' / 'res')
    elif typ == 'studio':
        roots.append(app_dir / 'app' / 'src' / 'main' / 'res')
    elif typ == 'eclipse':
        roots.append(app_dir / 'res')
    return [root for root in roots if root.exists()]


def _source_dirs(app_dir, typ):
    roots = []
    src = get_android_src_dir(app_dir, typ)
    if src and src.exists():
        roots.append(src)
    if typ == 'studio':
        kt = app_dir / 'app' / 'src' / 'main' / 'kotlin'
        if kt.exists() and kt not in roots:
            roots.append(kt)
    return roots


def _sample_path(value, mode='exact'):
    path = (value or '').strip()
    if not path:
        return ''
    path = path.replace('.*', 'sample').replace('*', 'sample')
    path = path.replace('.+', 'sample')
    path = re.sub(r'[?+|^$()\[\]\\]', '', path)
    if mode == 'prefix':
        if not path.endswith('/'):
            path = f'{path}/'
        path = f'{path}sample'
    if not path.startswith('/'):
        path = f'/{path}'
    return path


def _path_matches(patterns, prefixes, exacts, path):
    if exacts and path in exacts:
        return True
    if prefixes and any(path.startswith(prefix) for prefix in prefixes):
        return True
    for pattern in patterns:
        regex = re.escape(pattern)
        regex = regex.replace(r'\.\*', '.*').replace(r'\*', '.*')
        try:
            if re.fullmatch(regex, path):
                return True
        except re.error:
            continue
    return not (patterns or prefixes or exacts)


def _enumerate_candidate_urls(filter_details):
    schemes = filter_details.get('schemes', [])
    hosts = filter_details.get('hosts', [])
    ports = filter_details.get('ports', [])
    paths = [_sample_path(path) for path in filter_details.get('paths', [])]
    prefixes = [
        _sample_path(prefix, mode='prefix')
        for prefix in filter_details.get('path_prefixs', [])
    ]
    patterns = [
        _sample_path(pattern)
        for pattern in filter_details.get('path_patterns', [])
    ]
    path_candidates = [path for path in paths + prefixes + patterns if path]
    if not path_candidates:
        path_candidates = ['']
    if not hosts:
        hosts = ['']
    if not ports:
        ports = ['']
    urls = []
    for scheme in schemes:
        scheme_prefix = scheme if scheme.endswith('://') else f'{scheme}://'
        for host in hosts:
            for port in ports:
                host_part = host
                if host_part and port:
                    host_part = f'{host_part}:{port}'
                for path in path_candidates:
                    if host_part:
                        urls.append(f'{scheme_prefix}{host_part}{path}')
                    elif path:
                        urls.append(f'{scheme_prefix}{path.lstrip("/")}')
                    else:
                        urls.append(scheme_prefix)
    return _dedupe(urls)[:MAX_CANDIDATE_URLS]


def _scan_lines(relative_path, lines, kind='code'):
    candidates = []
    handlers = []
    component_hints = _component_hints_from_path(relative_path)
    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        for handler_kind, needle in HANDLER_HINTS.items():
            if needle in line:
                handlers.append({
                    'kind': handler_kind,
                    'location': f'{relative_path}:{line_no}',
                    'snippet': line[:200],
                    'component_hints': component_hints,
                })
        regexes = [DEEPLINK_LITERAL_REGEX]
        if kind == 'xml':
            regexes = [NAV_DEEPLINK_REGEX, DEEPLINK_LITERAL_REGEX]
        for regex in regexes:
            for match in regex.finditer(line):
                if regex is NAV_DEEPLINK_REGEX:
                    raw_uri = match.group(1)
                else:
                    raw_uri = match.group('uri')
                uri = _clean_uri(raw_uri)
                if not _is_deeplink_uri(uri):
                    continue
                if regex is NAV_DEEPLINK_REGEX:
                    candidate_kind = 'navigation_xml'
                else:
                    candidate_kind = 'uri_literal'
                candidates.append({
                    'uri': uri,
                    'kind': candidate_kind,
                    'location': f'{relative_path}:{line_no}',
                    'snippet': line[:200],
                    'component_hints': component_hints,
                })
    return candidates, handlers


def _aggregate_code_candidates(candidates):
    aggregated = {}
    for candidate in candidates:
        entry = aggregated.setdefault(candidate['uri'], {
            'uri': candidate['uri'],
            'kinds': set(),
            'locations': [],
            'snippets': [],
            'component_hints': set(),
            'matched_components': set(),
        })
        entry['kinds'].add(candidate['kind'])
        entry['component_hints'].update(candidate['component_hints'])
        entry['locations'].append(candidate['location'])
        if candidate['snippet']:
            entry['snippets'].append(candidate['snippet'])
    return aggregated


def _scan_code_and_resources(checksum, app_dic):
    app_dir = Path(app_dic['app_dir'])
    app_type = app_dic['zipped']
    msg = 'Extracting deeplink candidates from Android source and resources'
    logger.info(msg)
    append_scan_status(checksum, msg)
    candidates = []
    handlers = []
    for src_dir in _source_dirs(app_dir, app_type):
        for file_path in src_dir.rglob('*'):
            if (file_path.suffix not in SCANNED_SOURCE_EXTENSIONS
                    or not file_path.is_file()):
                continue
            try:
                content = file_path.read_text('utf-8', 'ignore').splitlines()
            except Exception:
                continue
            relative_path = file_path.relative_to(app_dir).as_posix()
            file_candidates, file_handlers = _scan_lines(relative_path, content)
            candidates.extend(file_candidates)
            handlers.extend(file_handlers)
    for res_dir in _resource_dirs(app_dir, app_type):
        for file_path in res_dir.rglob('*'):
            if (file_path.suffix not in SCANNED_RESOURCE_EXTENSIONS
                    or not file_path.is_file()):
                continue
            try:
                content = file_path.read_text('utf-8', 'ignore').splitlines()
            except Exception:
                continue
            relative_path = file_path.relative_to(app_dir).as_posix()
            file_candidates, _ = _scan_lines(relative_path, content, kind='xml')
            candidates.extend(file_candidates)
    return _aggregate_code_candidates(candidates), handlers


def _build_manifest_entries(man_an_dic):
    exported = set(man_an_dic.get('exported_act', []))
    entries = []
    for component, details in man_an_dic.get('browsable_activities', {}).items():
        filters = details.get('filters', [])
        if not filters:
            filters = [{
                'schemes': details.get('schemes', []),
                'hosts': details.get('hosts', []),
                'ports': details.get('ports', []),
                'paths': details.get('paths', []),
                'path_prefixs': details.get('path_prefixs', []),
                'path_patterns': details.get('path_patterns', []),
            }]
        candidate_urls = []
        for filter_details in filters:
            candidate_urls.extend(_enumerate_candidate_urls(filter_details))
        entries.append({
            'component': component,
            'exported': component in exported,
            'external_reachability': (
                'reachable'
                if component in exported
                else 'not_exported'
            ),
            'confidence': 'high' if component in exported else 'low',
            'match_reason': (
                'BROWSABLE activity is exported through the manifest'
                if component in exported
                else 'BROWSABLE activity exists but is not exported'
            ),
            'schemes': details.get('schemes', []),
            'hosts': details.get('hosts', []),
            'ports': details.get('ports', []),
            'paths': details.get('paths', []),
            'path_prefixs': details.get('path_prefixs', []),
            'path_patterns': details.get('path_patterns', []),
            'candidate_urls': _dedupe(candidate_urls)[:MAX_CANDIDATE_URLS],
            'handler_locations': [],
            'literal_locations': [],
            'code_literals': [],
            'filters': filters,
        })
    return entries


def _uri_matches_manifest(candidate_uri, manifest_entry):
    if candidate_uri.startswith('intent://'):
        return False
    parsed = urlparse(candidate_uri)
    if not parsed.scheme:
        return False
    schemes = [_strip_scheme_separator(scheme) for scheme in manifest_entry['schemes']]
    if schemes and parsed.scheme not in schemes:
        return False
    if manifest_entry['hosts']:
        candidate_host = parsed.hostname or parsed.netloc
        normalized_hosts = []
        for host in manifest_entry['hosts']:
            normalized_hosts.append(host.replace('*.', '').replace('#', ''))
        if candidate_host not in normalized_hosts:
            return False
    if manifest_entry['ports']:
        port = str(parsed.port or '')
        if port not in [str(item) for item in manifest_entry['ports']]:
            return False
    return _path_matches(
        manifest_entry['path_patterns'],
        manifest_entry['path_prefixs'],
        manifest_entry['paths'],
        parsed.path or '/',
    )


def _attach_code_evidence(manifest_entries, code_candidates, handlers):
    for handler in handlers:
        for entry in manifest_entries:
            if _component_matches(entry['component'], handler['component_hints']):
                entry['handler_locations'].append(
                    f"{handler['location']} [{handler['kind']}]")
    for uri, candidate in code_candidates.items():
        for entry in manifest_entries:
            uri_match = _uri_matches_manifest(uri, entry)
            component_match = _component_matches(
                entry['component'], candidate['component_hints'])
            if not (uri_match or component_match):
                continue
            candidate['matched_components'].add(entry['component'])
            entry['literal_locations'].extend(candidate['locations'])
            if len(entry['code_literals']) < MAX_EVIDENCE_ITEMS:
                entry['code_literals'].append(uri)


def _serialize_manifest_entries(entries, include_unreachable=False):
    serialized = []
    for entry in entries:
        if not include_unreachable and entry['external_reachability'] != 'reachable':
            continue
        serialized.append({
            'component': entry['component'],
            'exported': entry['exported'],
            'external_reachability': entry['external_reachability'],
            'confidence': entry['confidence'],
            'match_reason': entry['match_reason'],
            'schemes': _dedupe(entry['schemes']),
            'hosts': _dedupe(entry['hosts']),
            'ports': _dedupe(entry['ports']),
            'paths': _dedupe(entry['paths']),
            'path_prefixs': _dedupe(entry['path_prefixs']),
            'path_patterns': _dedupe(entry['path_patterns']),
            'candidate_urls': _dedupe(entry['candidate_urls']),
            'handler_locations': _dedupe(
                entry['handler_locations'])[:MAX_EVIDENCE_ITEMS],
            'literal_locations': _dedupe(
                entry['literal_locations'])[:MAX_EVIDENCE_ITEMS],
            'code_literals': _dedupe(entry['code_literals'])[:MAX_EVIDENCE_ITEMS],
        })
    return serialized


def _serialize_code_candidates(code_candidates):
    serialized = []
    for uri, candidate in code_candidates.items():
        matched_components = sorted(candidate['matched_components'])
        if matched_components:
            continue
        serialized.append({
            'uri': uri,
            'confidence': 'low',
            'external_reachability': 'unknown',
            'kind': ', '.join(sorted(candidate['kinds'])),
            'candidate_urls': [uri],
            'locations': _dedupe(candidate['locations'])[:MAX_EVIDENCE_ITEMS],
            'matched_components': matched_components,
        })
    return serialized


def _serialize_handlers(handlers):
    serialized = []
    seen = set()
    for handler in handlers:
        key = (handler['location'], handler['kind'])
        if key in seen:
            continue
        seen.add(key)
        serialized.append({
            'kind': handler['kind'],
            'location': handler['location'],
            'snippet': handler['snippet'],
        })
    return serialized[:MAX_PROBE_TARGETS]


def _build_probe_targets(reachable_entries, code_candidates):
    targets = []
    for entry in reachable_entries:
        for url in entry['candidate_urls']:
            targets.append({
                'url': url,
                'source': 'manifest',
                'component': entry['component'],
                'confidence': entry['confidence'],
            })
    for uri, candidate in code_candidates.items():
        if candidate['matched_components']:
            continue
        targets.append({
            'url': uri,
            'source': 'code',
            'component': '',
            'confidence': 'low',
        })
    deduped = []
    seen = set()
    for target in targets:
        if target['url'] in seen:
            continue
        seen.add(target['url'])
        deduped.append(target)
    return deduped[:MAX_PROBE_TARGETS]


def analyze_deeplinks(checksum, app_dic, man_an_dic):
    """Create a best-effort merged deeplink inventory."""
    inventory = {
        'summary': {
            'reachable_count': 0,
            'candidate_count': 0,
            'handler_count': 0,
            'probe_target_count': 0,
        },
        'reachable': [],
        'candidates': [],
        'handlers': [],
        'probe_targets': [],
        'notes': [
            (
                'Manifest reachability is best-effort and based on '
                'exported + BROWSABLE analysis.'
            ),
            (
                'Code-derived deeplink candidates cannot guarantee '
                'external reachability without dynamic validation.'
            ),
        ],
    }
    try:
        manifest_entries = _build_manifest_entries(man_an_dic)
        code_candidates, handlers = _scan_code_and_resources(checksum, app_dic)
        _attach_code_evidence(manifest_entries, code_candidates, handlers)
        reachable = _serialize_manifest_entries(manifest_entries)
        manifest_candidates = _serialize_manifest_entries(
            manifest_entries, include_unreachable=True)
        unreachable = [
            entry for entry in manifest_candidates
            if entry['external_reachability'] != 'reachable'
        ]
        code_only = _serialize_code_candidates(code_candidates)
        probe_targets = _build_probe_targets(reachable, code_candidates)
        inventory['reachable'] = reachable
        inventory['candidates'] = unreachable + code_only
        inventory['handlers'] = _serialize_handlers(handlers)
        inventory['probe_targets'] = probe_targets
        inventory['summary'] = {
            'reachable_count': len(reachable),
            'candidate_count': len(inventory['candidates']),
            'handler_count': len(inventory['handlers']),
            'probe_target_count': len(probe_targets),
        }
        return inventory
    except Exception as exp:
        msg = 'Failed to analyze Android deeplinks'
        logger.exception(msg)
        append_scan_status(checksum, msg, repr(exp))
        return inventory


def _normalize_inventory_entry(entry):
    """Backfill optional deeplink inventory fields for legacy records."""
    normalized = dict(entry or {})
    uri = normalized.get('uri', '')
    candidate_urls = normalized.get('candidate_urls')
    if candidate_urls is None:
        candidate_urls = [uri] if uri else []
    normalized['candidate_urls'] = _dedupe(candidate_urls)
    for key in (
        'locations',
        'handler_locations',
        'literal_locations',
        'code_literals',
        'matched_components',
    ):
        value = normalized.get(key)
        if not value:
            normalized[key] = []
        else:
            normalized[key] = _dedupe(value)
    if 'confidence' not in normalized:
        normalized['confidence'] = ''
    if 'external_reachability' not in normalized:
        normalized['external_reachability'] = 'unknown'
    return normalized


def normalize_deeplink_inventory(inventory):
    """Normalize deeplink inventory shape for templates and APIs."""
    source = dict(inventory or {})
    reachable = [
        _normalize_inventory_entry(entry)
        for entry in source.get('reachable', [])
    ]
    candidates = [
        _normalize_inventory_entry(entry)
        for entry in source.get('candidates', [])
    ]
    handlers = list(source.get('handlers', []))
    probe_targets = list(source.get('probe_targets', []))
    notes = list(source.get('notes', []))
    summary = dict(source.get('summary', {}))
    summary.setdefault('reachable_count', len(reachable))
    summary.setdefault('candidate_count', len(candidates))
    summary.setdefault('handler_count', len(handlers))
    summary.setdefault('probe_target_count', len(probe_targets))
    return {
        'summary': summary,
        'reachable': reachable,
        'candidates': candidates,
        'handlers': handlers,
        'probe_targets': probe_targets,
        'notes': notes,
    }
