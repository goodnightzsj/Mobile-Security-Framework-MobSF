# -*- coding: utf_8 -*-
"""Middleware for legacy HTML UI localization."""

from .ui_localizer import localize_html
from .ui_localizer import should_localize


class UiTranslationMiddleware:
    """Translate rendered HTML pages for the active UI language."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(response, 'streaming', False):
            return response
        content_type = response.get('Content-Type', '')
        language = getattr(request, 'LANGUAGE_CODE', '')
        if 'text/html' not in content_type or not should_localize(language):
            return response
        charset = response.charset or 'utf-8'
        html = response.content.decode(charset, errors='ignore')
        response.content = localize_html(html, language).encode(charset)
        return response
