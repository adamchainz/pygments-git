from __future__ import annotations

import re

from pygments.lexer import bygroups
from pygments.lexer import RegexLexer
from pygments.lexer import using
from pygments.lexers.diff import DiffLexer
from pygments.lexers.shell import BashLexer
from pygments.token import Comment
from pygments.token import Generic
from pygments.token import Keyword
from pygments.token import Literal
from pygments.token import Name
from pygments.token import Number
from pygments.token import Operator
from pygments.token import Punctuation
from pygments.token import String
from pygments.token import Text


class GitAttributesLexer(RegexLexer):
    name = "Git Attributes"
    aliases = ("git-attributes",)
    flags = re.MULTILINE

    tokens = {
        "root": [
            (r"^#.*$", Comment),
            (
                r"^(\S+)(\s+)",
                bygroups(Literal, Text),  # type: ignore[no-untyped-call]
                "attributes",
            ),
            (r"^.*\n", Text),
        ],
        "attributes": [
            (
                r"(-)?(.+?)(=)([^ \t\n]+)",
                bygroups(  # type: ignore[no-untyped-call]
                    Operator, Name.Variable, Operator, String.Symbol
                ),
            ),
            (
                r"(-)?([^ \t\n]+)",
                bygroups(Operator, Name.Variable),  # type: ignore[no-untyped-call]
            ),
            (r"[ \t]+", Text),
            (r"$", Text, "#pop"),
        ],
    }


class GitCommitEditMsgLexer(RegexLexer):
    name = "Git Commit Edit-Msg"
    aliases = ("git-commit-edit-msg",)
    flags = re.MULTILINE

    tokens = {
        "root": [
            (
                r"^(# On branch )(.*)$",
                bygroups(Comment, Name.Label),  # type: ignore [no-untyped-call]
            ),
            (r"^#.*\n", Comment),
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
                    Text,
                    Number.Hex,
                    Text,
                ),
            ),
            (r"^(?=@@ )", Generic.Subheading, "diff"),
            # Everything else
            (r".*\n", Text),
        ],
        "diff": [
            (
                r"(?s).*",
                using(DiffLexer),  # type: ignore [no-untyped-call]
                "#pop",
            ),
        ],
    }


class GitConflictMarkersLexer(RegexLexer):
    name = "Git Conflict Markers"
    aliases = ("git-conflict-markers",)
    flags = re.MULTILINE

    tokens = {
        "root": [
            (
                r"^(<{7})( )?(.+)?$",
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker, Text, Name.Label
                ),
            ),
            (
                r"""(?x)
                    ^
                    (\|{7})
                    (\ parent\ of\ )
                    ([0-9a-f]{7})
                    (\ \()
                    (.*?)
                    (\))
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker,
                    Name.Label,
                    Number.Hex,
                    Text,
                    Name.Label,
                    Text,
                ),
            ),
            (
                r"^(\|{7})( )?(.*)$",
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker, Text, Name.Label
                ),
            ),
            (
                r"^(={7})( )?(.*)$",
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker, Text, Name.Label
                ),
            ),
            (
                r"""(?x)
                    ^
                    (>{7})
                    (\ )
                    ([0-9a-f]{7})
                    (\ \()
                    (.*?)
                    (\))
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker, Text, Number.Hex, Text, Name.Label, Text
                ),
            ),
            (
                r"^(>{7})(\ )?(.*)?$",
                bygroups(  # type: ignore [no-untyped-call]
                    Punctuation.Marker, Text, Name.Label
                ),
            ),
            (r".*\n", Text),
        ]
    }


class GitBashSessionLexer(RegexLexer):
    name = "Git Bash Session"
    aliases = ("git-console",)
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
                    Number.Hex, Generic.Output, Name.Label, Name.Tag
                ),
            ),
            # git log --oneline
            (
                r"""(?x)
                    ^
                    ([|/\\ ]*\*\ )?  # --graph
                    ([0-9a-f]{7})
                    (\ )
                    (\(.*?\) )?
                    (.*)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Generic.Output,
                    Number.Hex,
                    Generic.Output,
                    Name.Label,
                    Generic.Output,
                ),
            ),
            # git log
            (
                r"^(commit)( )([0-9a-f]{40})( \(.*?\))?$",
                bygroups(  # type: ignore [no-untyped-call]
                    Generic.Subheading,
                    Generic.Output,
                    Number.Hex,
                    Name.Label,
                ),
            ),
            (
                r"""(?x)
                    ^
                    ((?:Author|AuthorDate|Commit|CommitDate|Date):)
                    (\ +)
                    (.*)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword.Declaration,
                    Generic.Output,
                    String.Symbol,
                ),
            ),
            (
                r"""(?x)
                    ^
                    (Merge:)
                    (\ +)
                    (.*)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword.Declaration,
                    Generic.Output,
                    Number.Hex,
                ),
            ),
            (
                r"""(?xi)
                    ^
                    (\ *)
                    ((?:co-authored|signed-off)-by:)
                    (\ +)
                    (.*)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Generic.Output,
                    Keyword.Declaration,
                    Generic.Output,
                    String.Symbol,
                ),
            ),
            # git commit
            (
                r"^(\[main )([0-9a-f]{7})(\])(.*)$",
                bygroups(  # type: ignore [no-untyped-call]
                    Name.Label,
                    Number.Hex,
                    Name.Label,
                    Generic.Output,
                ),
            ),
            # hints and errors
            (r"^hint:.*$", Comment.Single),
            (r"^(error|fatal):.*$", Generic.Error),
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


class GitIgnoreLexer(RegexLexer):
    name = "Git Ignore"
    aliases = ("git-ignore",)
    flags = re.MULTILINE

    tokens = {
        "root": [
            (r"^#.*$", Comment),
            (r"^", Text, "pattern"),
        ],
        "pattern": [
            (r"\\!", Text),
            (r"([!?*]|\*\*)", Keyword),
            (
                r"(\[)(.*?)(\])",
                bygroups(Keyword, Text, Keyword),  # type: ignore [no-untyped-call]
            ),
            (r"\n", Text, "#pop"),
            (r".", Text),
        ],
    }


class GitRebaseTodoLexer(RegexLexer):
    name = "Git Rebase TODO"
    aliases = ("git-rebase-todo",)
    flags = re.MULTILINE

    tokens = {
        "root": [
            (
                r"""(?x)
                    ^
                    (x|exec)
                    (\ )
                """,
                bygroups(Keyword, Text),  # type: ignore [no-untyped-call]
                "command",
            ),
            (
                r"""(?x)
                    ^
                    (b|break)
                    (\ +)?
                    (\#.*?)?
                    $
                """,
                bygroups(Keyword, Text, Comment),  # type: ignore [no-untyped-call]
            ),
            (
                r"""(?x)
                    ^
                    (l|label|t|reset)
                    (\ +)
                    (.*?)
                    (\#.*?)?
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword, Text, Name.Label, Comment
                ),
            ),
            (
                r"""(?x)
                    ^
                    (m|merge)
                    (\ +)
                    (?:
                        (-[Cc]\ )
                        ([0-9a-f]{7})
                    )?
                    (\ +)
                    (.*?)
                    (\#.*?)?
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword, Text, Keyword, Number.Hex, Text, Name.Label, Comment
                ),
            ),
            (
                r"""(?x)
                    ^
                    ([a-z]+(?:\ -[Cc])?)
                    (\ )
                    ([0-9a-f]{7})
                    (\ .*?|)
                    (\#.*)?
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword, Text, Number.Hex, Text, Comment
                ),
            ),
            (
                r"""(?x)
                    ^
                    (update-ref)
                    (\ )
                    (.*?)
                    (\#.*)?
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Keyword, Text, Name.Label, Comment
                ),
            ),
            (
                r"""(?x)
                    ^
                    (\#\ Rebase\ )
                    ([0-9a-f]{7})
                    (\.\.)
                    ([0-9a-f]{7})
                    (\ onto\ )
                    ([0-9a-f]{7})
                    (.*)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Comment,
                    Number.Hex,
                    Comment,
                    Number.Hex,
                    Comment,
                    Number.Hex,
                    Comment,
                ),
            ),
            (
                r"""(?x)
                    ^
                    (\#\ )
                    ([a-z])
                    (,\ )
                    ([a-z-]+)
                    (\ .*?)
                    (\ =\ .*|$)
                    $
                """,
                bygroups(  # type: ignore [no-untyped-call]
                    Comment,
                    Keyword,
                    Comment,
                    Keyword,
                    Name.Variable,
                    Comment,
                ),
            ),
            (r"^#.*\n", Comment),
            (r".*\n", Text),
        ],
        "command": [
            (r".*$", using(BashLexer), "#pop"),  # type: ignore [no-untyped-call]
        ],
    }
