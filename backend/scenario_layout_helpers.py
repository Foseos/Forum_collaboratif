"""Presentation helpers shared by the scenario maintenance scripts."""

from html import escape
from html.parser import HTMLParser


def p(text):
    return '<p style="margin:0 0 .9rem;line-height:1.85;">' + escape(text) + '</p>'


def section(title, body):
    return '<section style="margin:1rem 0;border:1px solid rgba(124,58,237,.3);border-radius:8px;overflow:hidden;"><div style="padding:.65rem 1rem;background:rgba(124,58,237,.16);"><h2 style="margin:0;font-size:1rem;color:#c4b5fd;">' + escape(title) + '</h2></div><div style="padding:1rem;">' + body + '</div></section>'


class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    def handle_starttag(self, tag, attrs):
        if tag not in ('img', 'br', 'hr', 'input', 'meta', 'link'):
            self.stack.append(tag)
    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, 'Invalid nesting: ' + tag
