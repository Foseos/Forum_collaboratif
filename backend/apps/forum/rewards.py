import re
from html.parser import HTMLParser

from .arcana import credit


class MessageTextParser(HTMLParser):
    boundaries = {'p', 'div', 'br', 'li', 'ul', 'ol', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'tr', 'hr', 'section', 'pre'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.hidden += 1
        if tag in self.boundaries:
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.hidden = max(0, self.hidden - 1)
        if tag in self.boundaries:
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def count_message_words(content):
    parser = MessageTextParser()
    parser.feed(content)
    parser.close()
    return len(re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", ''.join(parser.parts)))


def award_publication(post):
    """Called once on publication, inside the post creation transaction."""
    if count_message_words(post.content) > 100:
        credit(post.author_id, 10, f'Publication : {post.topic.title[:170]}')
