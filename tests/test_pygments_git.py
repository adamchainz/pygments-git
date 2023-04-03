from __future__ import annotations

from html import escape as e
from html.parser import HTMLParser
from pathlib import Path
from textwrap import dedent

import pytest
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

MODULE_DIR = Path(__file__).parent.resolve()
formatter = HtmlFormatter()


@pytest.fixture(scope="module")
def golden_file(request):
    index = MODULE_DIR / "index.html"

    parser = TestTableParser()
    parser.feed(index.read_text())

    print(parser.rows)
    1 / 0

    class Checker:
        def __init__(self):
            self.cases: list[tuple[str, str, str, str]] = []

        def check(self, testid: str, lexer: str, given: str):
            given = dedent(given)
            result = highlight(
                given,
                lexer=get_lexer_by_name(lexer, stripnl=False),
                formatter=formatter,
            )
            self.cases.append((lexer, testid, given, result))

    checker = Checker()

    yield checker

    if not request.config.getoption("--save"):
        return

    lines = [
        "<!doctype html>",
        "<html>",
        "<head>",
        f"<style>{formatter.get_style_defs('.highlight')}</style>",
        "</head>",
        "<body>",
        "<table>",
        "<thead>",
        "<tr>",
        "<th>ID</th>",
        "<th>Lexer</th>",
        "<th>Input</th>",
        "<th>Output</th>",
        "</tr>",
        "</thead>",
        "<tbody>",
    ]
    for lexer, testid, given, result in checker.cases:
        lines.extend(
            [
                "<tr>",
                "<td>",
                e(testid),
                "</td>",
                "<td>",
                e(lexer),
                "</td>",
                "<td>",
                "<code>",
                "<pre>",
                e(given),
                "</pre>",
                "</code>",
                "</td>",
                "<td>",
                "<code class=highlight>",
                "<pre>",
                result,
                "</pre>",
                "</code>",
                "</td>",
                "</tr>",
            ]
        )
    lines.extend(
        [
            "</tbody>",
            "</table>",
            "</body>",
            "</html>",
        ]
    )

    index.write_text("\n".join(lines))


class TestTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.seen_thead = False
        self.current_row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif self.in_table and self.seen_thead and tag == "tr":
            self.in_row = True
            self.current_row = []

    def handle_data(self, data):
        if self.in_row:
            data = data.strip()
            if data:
                self.current_row.append(data)

    def handle_endtag(self, tag):
        if self.in_table and tag == "thead":
            self.seen_thead = True
        if self.in_table and tag == "tr":
            self.in_row = False
            if self.current_row:
                self.rows.append(tuple(self.current_row))
        elif tag == "table":
            self.in_table = False


def test_git_console(golden_file):
    golden_file.check(
        "test_git_console",
        "git-console",
        """\
        $ git reflog
        819b03d (HEAD -> main, origin/main) HEAD@{0}: commit: Bop it
        414a4ce HEAD@{1}: commit (amend): Twist it
        $ git log --oneline 'main'
        819b03d Bop it
        414a4ce Twist it
        """,
    )


#     session =

#     result = highlight_html("git-console", session)

#     assert result == (
#         '<div class="highlight"><pre>'
#         "<span></span>"
#         '<span class="gp">$ </span>git<span class="w"> </span>reflog\n'
#         '<span class="mh">819b03d</span><span class="go"> (HEAD -&gt; main, origin/main) HEAD@{0}: commit: Bop it</span>\n'
#         '<span class="mh">414a4ce</span> <span class="nt">HEAD@{1}:</span><span class="go"> commit (amend): Twist it</span>\n'
#         '<span class="gp">$ </span>git<span class="w"> </span>log<span class="w"> </span>--oneline<span class="w"> </span><span class="s1">&#39;main&#39;</span>\n'
#         '<span class="mh">819b03d</span><span class="go"> Bop it</span>\n'
#         '<span class="mh">414a4ce</span><span class="go"> Twist it</span>\n</pre></div>\n'
#     )
