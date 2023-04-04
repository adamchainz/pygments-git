from __future__ import annotations

from html import escape as e
from pathlib import Path
from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

MODULE_DIR = Path(__file__).parent.resolve()
formatter = HtmlFormatter(style="colorful")


@pytest.fixture(scope="module")
def golden_file(request):
    save = request.config.getoption("--save")

    index = MODULE_DIR / "index.html"

    text = index.read_text()
    soup = BeautifulSoup(text, "html.parser")
    loaded_cases: dict[str, tuple[str, str, str]] = {}
    for row in soup.find("tbody").find_all("tr"):
        tds = iter(row.find_all("td"))
        testid = next(tds).get_text().strip()
        lexer = next(tds).get_text().strip()
        given = next(tds).get_text().strip()
        result = str(next(tds).find("div", {"class": "highlight"})).strip()
        loaded_cases[testid] = (lexer, given, result)

    class Checker:
        def __init__(self) -> None:
            self.cases: dict[str, tuple[str, str, str]] = {}

        def check(self, testid: str, lexer: str, given: str) -> None:
            given = dedent(given).rstrip("\n")
            result = highlight(
                given,
                lexer=get_lexer_by_name(lexer, stripnl=False),
                formatter=formatter,
            )
            result = str(BeautifulSoup(result, "html.parser")).strip()
            self.cases[testid] = (lexer, given, result)
            if not save and testid in loaded_cases:  # pragma: no branch
                loaded_lexer, loaded_given, loaded_result = loaded_cases[testid]
                if lexer == loaded_lexer and given == loaded_given:  # pragma: no branch
                    assert result == loaded_result

    checker = Checker()

    yield checker

    if save:  # pragma: no cover
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
        for testid, (lexer, given, result) in checker.cases.items():
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
                    result,
                    "</td>",
                    "</tr>",
                ]
            )
        lines.extend(
            [
                "</tbody>",
                "</table>",
                "</body>",
                "</html>\n",
            ]
        )

        index.write_text("\n".join(lines))


def test_git_console(golden_file):
    golden_file.check(
        "test_git_console",
        "git-console",
        """\
        $ git reflog
        0e87b4d (HEAD -> main, origin/main) HEAD@{0}: commit: Bop it
        414a4ce HEAD@{1}: commit (amend): Twist it
        $ git log --oneline 'main'
        0e87b4d (HEAD -> main, origin/main) Bop it
        414a4ce Twist it
        $ git log --graph --oneline
        * 0e87b4d (HEAD -> main, origin/main) Bop it
        * 414a4ce Twist it
        $ git log --patch -n 1
        commit 0e87b4d49a0c48fd29b1b1c400ac7ebeabeb535d (HEAD -> main)
        Author: A Hacker <hacker@example.com>
        Date:   Tue Apr 4 11:32:10 2023 +0100

            Bop it

        diff --git it.txt it.txt
        index 3eb29f0..ed3581b 100644
        --- it.txt
        +++ it.txt
        @@ -1 +1 @@
        -twisted
        +bopped
        """,
    )
