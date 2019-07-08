import unittest
from tagged import tag, ParseError


@tag
def t(strings, values):
    return strings, values


class TestTag(unittest.TestCase):
    def test_escaping(self):
        self.assertEqual(t("a{{1}}a"), (("a{1}a",), ()))
        self.assertEqual(t("a{{{1}}}a"), (("a{", "}a"), (1,)))
        self.assertEqual(t("a{({1})}a"), (("a", "a"), ({1},)))

    def test_expressions(self):
        x = 1
        self.assertEqual(t("{x}a{x}"), (("", "a", ""), (x, x)))

    def test_unterminated_expression(self):
        with self.assertRaisesRegex(ParseError, "unterminated expression"):
            t("a{1")

    def test_statement(self):
        with self.assertRaises(SyntaxError):
            t("a{if True: pass}")

    def test_caching(self):
        def _t(strings, values):
            return strings

        cached = tag(_t)
        self.assertIs(cached("a{1}a"), cached("a{1}a"))

        another_cached = tag(_t)
        self.assertIsNot(another_cached("a{1}a"), cached("a{1}a"))

        not_cached = tag(_t, cache_maxsize=0)
        self.assertIsNot(not_cached("a{1}a"), not_cached("a{1}a"))


if __name__ == "__main__":
    unittest.main()
