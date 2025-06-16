import sys
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

class SimpleHTMLValidator(HTMLParser):
    VOID_TAGS = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img',
        'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for (attr, value) in attrs:
                if attr == 'src':
                    self.images.append(value)
        if tag not in self.VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}>")
            return
        last = self.stack.pop()
        if last != tag:
            self.errors.append(f"Mismatched closing tag </{tag}> for <{last}>")

    def close(self):
        super().close()
        if self.stack:
            for tag in self.stack:
                self.errors.append(f"Unclosed tag <{tag}>")


def validate_html(path='index.html'):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = SimpleHTMLValidator()
    parser.feed(content)
    parser.close()
    return parser


def check_image_urls(urls):
    for url in urls:
        try:
            req = Request(url, method='HEAD')
            with urlopen(req) as resp:
                status = resp.status
            if status >= 400:
                print(f"Image URL {url} returned status {status}")
                return False
        except (URLError, HTTPError) as e:
            print(f"Failed to reach image URL {url}: {e}")
            return False
    return True


def main():
    parser = validate_html()
    if parser.errors:
        print('HTML validation errors:')
        for err in parser.errors:
            print(' -', err)
        sys.exit(1)
    if not parser.images:
        print('No image tags found to check.')
    else:
        if not check_image_urls(parser.images):
            sys.exit(1)
    print('All checks passed.')


if __name__ == '__main__':
    main()
