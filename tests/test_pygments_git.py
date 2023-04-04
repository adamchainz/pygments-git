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
        for testid, (lexer, given, result) in sorted(checker.cases.items()):
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
        | * 8b96195 (origin/twister, twister) Right foot red
        |/
        * f01aa9f Start the party
        |\\
        | * c3338de Another initial commit
        * 187c021 Initial commit

        $ git log --patch -n 1
        commit 0e87b4d49a0c48fd29b1b1c400ac7ebeabeb535d (HEAD -> main)
        Author: A Hacker <hacker@example.com>
        Date:   Tue Apr 4 11:32:10 2023 +0100

            Bop it

            Signed-off-by: A Hacker <hacker@example.com>

        diff --git it.txt it.txt
        index 3eb29f0..ed3581b 100644
        --- it.txt
        +++ it.txt
        @@ -1 +1 @@
        -twisted
        +bopped

        $ git commit -m "Spin it"
        [main 0bcdb8f] Spin it
        """,
    )


def test_git_rebase_todo(golden_file):
    golden_file.check(
        "test_git_rebase_todo",
        "git-rebase-todo",
        """\
        pick d05ab26 Flick it
        update-ref refs/heads/other

        # Rebase 7d2c29b..d05ab26 onto 7d2c29b (1 command)
        #
        # Commands:
        # p, pick <commit> = use commit
        # r, reword <commit> = use commit, but edit the commit message
        # e, edit <commit> = use commit, but stop for amending
        # s, squash <commit> = use commit, but meld into previous commit
        # f, fixup [-C | -c] <commit> = like "squash" but keep only the previous
        #                    commit's log message, unless -C is used, in which case
        #                    keep only this commit's message; -c is same as -C but
        #                    opens the editor
        # x, exec <command> = run command (the rest of the line) using shell
        # b, break = stop here (continue rebase later with 'git rebase --continue')
        # d, drop <commit> = remove commit
        # l, label <label> = label current HEAD with a name
        # t, reset <label> = reset HEAD to a label
        # m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
        #         create a merge commit using the original merge commit's
        #         message (or the oneline, if no original merge commit was
        #         specified); use -c <commit> to reword the commit message
        # u, update-ref <ref> = track a placeholder for the <ref> to be updated
        #                       to this position in the new commits. The <ref> is
        #                       updated at the end of the rebase
        #
        # These lines can be re-ordered; they are executed from top to bottom.
        #
        # If you remove a line here THAT COMMIT WILL BE LOST.
        #
        # However, if you remove everything, the rebase will be aborted.
        #
        """,
    )
