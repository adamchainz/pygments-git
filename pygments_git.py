from __future__ import annotations

import re

from pygments.lexer import RegexLexer
from pygments.lexer import bygroups
from pygments.lexer import using
from pygments.lexers.diff import DiffLexer
from pygments.lexers.shell import BashLexer
from pygments.token import Generic
from pygments.token import Name
from pygments.token import Number
from pygments.token import Text


class GitSessionLexer(RegexLexer):
    name = "Git Bash Session"
    aliases = ("git-console", "git-shell-session")
    flags = re.MULTILINE

    tokens = {
        "root": [
            # Command
            (r"^\$ ", Generic.Prompt, "command"),
            # git reflog
            (
                r"""(?x)
                    ^
                    ([0-9a-f]{7})
                    (\ )
                    (
                        \(
                        HEAD\ ->
                        \ [-\w_/]+
                        \)
                    \ )?
                    (
                        [-\w_/]+
                        @
                        \{.*?\}
                        :
                    )
                """,
                bygroups(Number.Hex, Text, Name.Label, Name.Tag),
            ),
            # git log --oneline
            (
                r"""(?x)
                    ^
                    ([0-9a-f]{7})
                    (\ )
                    (
                        \(
                        (HEAD\ ->\ )?
                        ([-\w_/]+)
                        \)
                    )
                """,
                bygroups(Number.Hex, Text, Name.Label),
            ),
            # Any SHA to be highlighted as such
            (r"\b([0-9a-f]{40}|[0-9a-f]{7})\b", Number.Hex),
            # Diff lines
            (r"^(?=@@ )", Generic.Subheading, "diff"),
            # (r"(-.*)(\n)", bygroups(Generic.Deleted, Whitespace)),
            # (r"(\+.*)(\n)", bygroups(Generic.Inserted, Whitespace)),
            # Everything else plain text
            (r".*\n", Generic.Output),
        ],
        "command": [
            (r".*$", using(BashLexer), "#pop"),
        ],
        "diff": [
            (r"(([@ -+].*|)\n)*", using(DiffLexer), "#pop"),
        ],
    }
