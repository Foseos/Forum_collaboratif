"""Nettoyage du HTML soumis par les membres avant affichage sur le forum."""

import nh3


MEMBER_HTML = nh3.Cleaner(
    tags={
        'a', 'b', 'blockquote', 'br', 'caption', 'code', 'dd', 'del', 'div',
        'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
        'li', 'ol', 'p', 'pre', 's', 'small', 'span', 'strike', 'strong', 'sub', 'sup',
        'table', 'tbody', 'td', 'th', 'thead', 'tr', 'u', 'ul',
    },
    clean_content_tags={'script', 'style', 'iframe', 'svg', 'math', 'form', 'template'},
    attributes={
        '*': {'class', 'style', 'title'},
        'a': {'href'},
        'img': {'src', 'alt', 'width', 'height'},
        'td': {'colspan', 'rowspan'},
        'th': {'colspan', 'rowspan'},
    },
    filter_style_properties={
        'background', 'background-color', 'border', 'border-bottom',
        'border-collapse', 'border-radius', 'border-top', 'color', 'display',
        'font-family', 'font-size', 'font-style', 'font-weight', 'height',
        'letter-spacing', 'line-height', 'margin', 'margin-bottom',
        'margin-left', 'margin-right', 'margin-top', 'max-width', 'min-height',
        'object-fit', 'overflow', 'padding', 'padding-bottom', 'padding-left',
        'padding-right', 'padding-top', 'text-align', 'text-decoration',
        'text-transform', 'vertical-align', 'white-space', 'width',
    },
    url_schemes={'http', 'https', 'mailto'},
    url_relative='pass_through',
)


def sanitize_member_html(value):
    return MEMBER_HTML.clean(value or '')
