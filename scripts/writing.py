#!/usr/bin/env python3
"""Refresh only the profile's writing block from the author's public RSS feed."""
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import argparse
import html
import json
import xml.etree.ElementTree as ET

START = '<!-- writing:start -->'
END = '<!-- writing:end -->'
FEED = 'https://angelodeleon.com/rss.xml'


def validate(items):
    if not items or len(items) > 5:
        raise ValueError('Expected one to five public articles.')
    result = []
    for item in items:
        title = ' '.join(item['title'].split())
        url = item['url']
        parsed = urlsplit(url)
        if (not title or len(title) > 220 or parsed.scheme != 'https'
                or parsed.netloc != 'angelodeleon.com' or not parsed.path.startswith('/writing/')
                or parsed.query or parsed.fragment):
            raise ValueError('Unexpected article title or destination.')
        result.append({'title': title, 'url': url})
    if len({x['url'] for x in result}) != len(result):
        raise ValueError('Duplicate articles.')
    return result


def parse_feed(data):
    tree = ET.fromstring(data)
    items = [{'title': item.findtext('title', ''), 'url': item.findtext('link', '')}
             for item in tree.findall('./channel/item')[:5]]
    return validate(items)


def update(source, items):
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError('Writing markers must appear exactly once.')
    a, b = source.index(START) + len(START), source.index(END)
    if a > b:
        raise ValueError('Writing markers are out of order.')
    lines = []
    for item in validate(items):
        title = html.escape(item['title']).replace('[', r'\[').replace(']', r'\]')
        lines.append(f"- [{title}]({item['url']})")
    return source[:a] + '\n' + '\n'.join(lines) + '\n' + source[b:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', type=Path)
    parser.add_argument('--apply', type=Path)
    parser.add_argument('--readme', type=Path, default=Path('README.md'))
    args = parser.parse_args()
    if args.fetch:
        with urlopen(Request(FEED, headers={'User-Agent': 'RaDeleon-profile-widgets'}), timeout=25) as response:
            if urlsplit(response.url).netloc != 'angelodeleon.com':
                raise ValueError('Unexpected RSS redirect.')
            data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError('RSS exceeded its size bound.')
        items = parse_feed(data)
        args.fetch.parent.mkdir(parents=True, exist_ok=True)
        args.fetch.write_text(json.dumps(items, indent=2) + '\n')
    if args.apply:
        items = json.loads(args.apply.read_text())
        result = update(args.readme.read_text(), items)
        args.readme.write_text(result)


if __name__ == '__main__':
    main()
