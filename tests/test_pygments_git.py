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
    for h2 in soup.find_all("h2"):
        testid = h2["id"]
        p = h2.find_next("p")
        lexer = p.get_text().strip()[len("Lexer: ") :]
        given_pre = p.find_next("pre")
        given = given_pre.get_text().strip()
        result_div = given_pre.find_next("div", {"class": "highlight"})
        result = str(result_div).strip()
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
                assert loaded_lexer == lexer
                assert loaded_given == given
                assert result == loaded_result

    checker = Checker()

    yield checker

    if save:  # pragma: no cover
        lines = [
            "<!doctype html>",
            "<html>",
            "<head>",
            "<title>pygments-git tests</title>",
            (
                '<link rel="icon" href="data:image/svg+xml,&lt;svg xmlns=%22'
                + "http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22&gt;"
                + "&lt;text y=%22.9em%22 font-size=%2290%22&gt;🎨&lt;/text&gt;"
                + '&lt;/svg&gt;">'
            ),
            "<style>",
            dedent(
                """\
                :root {
                  font-family: "PT Sans", sans-serif;
                }
                .compare {
                  display: grid;
                  grid-template-columns: repeat(2, 1fr);
                  grid-gap: 1rem;
                }
                pre {
                  background: #eee;
                  padding: 0.5rem;
                }
                """
            ),
            formatter.get_style_defs(".highlight"),
            dedent(
                """\
                .highlight .pm { /* Punctuation.Marker */
                    color: #540099;
                    font-weight: bold;
                }
                """
            ),
            "</style>",
            "</head>",
            "<body>",
            "<h1>Tests</h1>",
        ]
        for testid, (lexer, given, result) in sorted(checker.cases.items()):
            lines.extend(
                [
                    f"<h2 id={testid}>",
                    e(testid),
                    f"<a href=#{testid}>#</a>",
                    "</h2>",
                    "<p>",
                    f"Lexer: {e(lexer)}",
                    "</p>",
                    "<div class=compare>" "<code>",
                    "<pre>",
                    e(given),
                    "</pre>",
                    "</code>",
                    result,
                    "</div>",
                ]
            )
        lines.extend(
            [
                "</html>\n",
            ]
        )

        index.write_text("\n".join(lines))


def test_git_attributes(golden_file):
    golden_file.check(
        "test_git_attributes",
        "git-attributes",
        """\
        # Hello attributes
        *.txt       text
        *\ttext=auto
        *.sh        text eol=lf
        *.jpg -text
        *.ps1 text working-tree-encoding=UTF-16LE eol=CRLF
        """,
    )


def test_git_commit_edit_msg(golden_file):
    golden_file.check(
        "test_git_commit_edit_msg",
        "git-commit-edit-msg",
        """\
        Bop it

        # Please enter the commit message for your changes. Lines starting
        # with '#' will be ignored, and an empty message aborts the commit.
        #
        # On branch main
        # Changes to be committed:
        #   modified:   it.txt
        #
        # ------------------------ >8 ------------------------
        # Do not modify or remove the line above.
        # Everything below it will be ignored.
        diff --git it.txt it.txt
        index ed3581b..b27f6d4 100644
        --- it.txt
        +++ it.txt
        @@ -1 +1 @@
        -twisted
        +bopped
        """,
    )


def test_git_conflict_markers(golden_file):
    golden_file.check(
        "test_git_conflict_markers",
        "git-conflict-markers",
        """\
        <<<<<<< HEAD
        red
        ||||||| parent of 09fb2fb (Make it blue)
        yellow
        =======
        blue
        >>>>>>> 09fb2fb (Make it blue)

        <<<<<<< current
        teal
        ||||||| original
        cerulean
        ======= bla
        cyan
        >>>>>>> incoming

        <<<<<<<
        purple
        |||||||
        puce
        =======
        cerise
        >>>>>>>
        """,
    )


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

        $ git show 362fdb8
        commit 362fdb88072ca0259e9f6e0251b47af4d75e141c
        Merge: 8456fa3 722568d
        Author: A Hacker <hacker9001@funmail.example>
        Date:   ...

            Merge branch 'jig'

        $ git commit -m "Spin it"
        [main 0bcdb8f] Spin it

        $ git pull
        hint: You have divergent branches and need to specify how to reconcile them.
        hint: You can do so by running one of the following commands sometime before
        hint: your next pull:
        hint:
        hint:   git config pull.rebase false  # merge
        hint:   git config pull.rebase true   # rebase
        hint:   git config pull.ff only       # fast-forward only
        hint:
        hint: You can replace "git config" with "git config --global" to set a default
        hint: preference for all repositories. You can also pass --rebase, --no-rebase,
        hint: or --ff-only on the command line to override the configured default per
        hint: invocation.
        fatal: Need to specify how to reconcile divergent branches.
        """,
    )


def test_git_ignore(golden_file):
    golden_file.check(
        "test_git_ignore",
        "git-ignore",
        """\
        # Hello ignorance
        /apples.py
        *.pyc
        !apples.pyc
        \\!literal-exclamation.apple
        a??les.pyx
        [Aa]pples.txt

        fruits/**
        """,
    )


def test_git_rebase_todo(golden_file):
    golden_file.check(
        "test_git_rebase_todo",
        "git-rebase-todo",
        """\
        pick d05ab26 Flick it  # awesome
        f -C 414a4ce
        label bopped
        break  # pause
        merge -C 414a4ce twisted
        update-ref refs/heads/other #update
        exec echo 'rebase complete' | say

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
