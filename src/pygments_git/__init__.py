from __future__ import annotations

import re

from pygments.lexer import bygroups
from pygments.lexer import RegexLexer
from pygments.lexer import using
from pygments.lexers.diff import DiffLexer
from pygments.lexers.shell import BashLexer
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import Name
from pygments.token import Number
from pygments.token import String
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
                    (\(.*?\)\ )?
                    (
                        [-\w_/]+
                        @
                        \{.*?\}
                        :
                    )
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Number.Hex, Text, Name.Label, Name.Tag
                ),
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
                bygroups(  # type: ignore [no-untyped-call]
                    Number.Hex, Text, Name.Label
                ),
            ),
            # git log
            (
                r"^(commit)( )([0-9a-f]{40})( )(\(.*?\))?$",
                bygroups(  # type: ignore [no-untyped-call]
                    Generic.Subheading,
                    Generic.Output,
                    Number.Hex,
                    Generic.Output,
                    Name.Label,
                ),
            ),
            (
                r"""(?x)
                    ^
                    ((?:Author|Date|AuthorDate|Commit|CommitDate|Co-Authored-By|Signed-off-by):)
                    (\ +)
                    (.*)$
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword.Declaration,
                    Generic.Output,
                    String.Symbol,
                ),
            ),
            # Any SHA to be highlighted as such
            (r"\b([0-9a-f]{40}|[0-9a-f]{7})\b", Number.Hex),
            # Diff lines
            (r"^diff --git.*$", Generic.Heading),
            (
                r"""(?x)^
                    (index\ )
                    ([0-9a-f]{7})
                    (\.\.)
                    ([0-9a-f]{7})
                    (\ \d+)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Generic.Heading,
                    Number.Hex,
                    Generic.Output,
                    Number.Hex,
                    Generic.Output,
                ),
            ),
            (r"^(?=@@ )", Generic.Subheading, "diff"),
            # Everything else plain text
            (r".*\n", Generic.Output),
        ],
        "command": [
            (r".*$", using(BashLexer), "#pop"),  # type: ignore [no-untyped-call]
        ],
        "diff": [
            (
                r"(([@ +-].*|)\n)*",
                using(DiffLexer),  # type: ignore [no-untyped-call]
                "#pop",
            ),
        ],
    }
