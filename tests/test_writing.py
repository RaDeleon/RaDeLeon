import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from writing import parse_feed, update, validate


class WritingTests(unittest.TestCase):
    def test_update_preserves_everything_outside_the_markers(self):
        source = '# Original\n<!-- writing:start -->\nOld\n<!-- writing:end -->\nKeep my projects.'
        items = [{'title': 'A [bounded] <example>', 'url': 'https://angelodeleon.com/writing/example/'}]
        result = update(source, items)
        self.assertTrue(result.startswith('# Original\n<!-- writing:start -->\n'))
        self.assertTrue(result.endswith('<!-- writing:end -->\nKeep my projects.'))
        self.assertIn(r'A \[bounded\] &lt;example&gt;', result)

    def test_unexpected_destinations_are_rejected(self):
        for url in ['http://angelodeleon.com/writing/a/', 'https://evil.example/writing/a/',
                    'https://angelodeleon.com@evil.example/writing/a/', 'https://angelodeleon.com/contact/']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate([{'title': 'Title', 'url': url}])

    def test_ambiguous_markers_cannot_replace_a_profile(self):
        item = [{'title': 'Article', 'url': 'https://angelodeleon.com/writing/a/'}]
        for source in ['No markers', '<!-- writing:start --><!-- writing:start --><!-- writing:end -->',
                       '<!-- writing:end --><!-- writing:start -->']:
            with self.subTest(source=source), self.assertRaises(ValueError):
                update(source, item)

    def test_empty_feed_does_not_erase_existing_writing(self):
        with self.assertRaises(ValueError):
            parse_feed(b'<rss><channel /></rss>')


if __name__ == '__main__':
    unittest.main()
