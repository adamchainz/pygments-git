============
pygments-git
============

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/pygments-git/main.yml.svg?branch=main&style=for-the-badge
   :target: https://github.com/adamchainz/pygments-git/actions?workflow=CI

.. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
   :target: https://github.com/adamchainz/pygments-git/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/pygments-git.svg?style=for-the-badge
   :target: https://pypi.org/project/pygments-git/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

Pygments lexers for Git output and files.

----

**Get better at command line Git** with my book `Boost Your Git DX <https://adamchainz.gumroad.com/l/bygdx>`__.

----

Installation
============

Use **pip**:

.. code-block:: sh

    python -m pip install pygments-git

Python 3.9 to 3.14 supported.

Usage
=====

With the package installed, Pygments will autodiscover the below lexers.

When using Pygments directly, you can refer to them by name.
Within Sphinx/docutils, you can refer to them in ``code-block`` directives:

.. code-block:: restructuredtext

    .. code-block:: git-console

        $ git log --oneline
        82fbbd3 D'oh! Fix math proof
        91e9879 Aye carumba! Grammar mistake
        61c4c08 Cowabunga! Update bibliography

To preview the lexers, open the ``tests/index.html`` file within the repository.

``git-attributes``
------------------

A lexer for |.gitattributes files|__.

.. |.gitattributes files| replace:: ``.gitattributes`` files
__ https://git-scm.com/docs/gitattributes

``git-blame-ignore-revs``
-------------------------

A lexer for the file format used by |blame.ignoreRevsFile|__.
The de facto name for a repository-wide ignore file is ``.git-blame-ignore-revs``, as recognized `by GitHub <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-a-file#ignore-commits-in-the-blame-view>`__ and potentially other Git hosting services.

.. |blame.ignoreRevsFile| replace:: ``blame.ignoreRevsFile``
__ https://git-scm.com/docs/git-blame#Documentation/git-blame.txt-blameignoreRevsFile

``git-commit-edit-msg``
-----------------------

A lexer for the ``COMMIT_EDITMSG`` file that Git opens when you run ``git commit``.
It calls out to |DiffLexer|__ for highlighting any diff, as added by |git commit --verbose|__.

.. |DiffLexer| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer

.. |git commit --verbose| replace:: ``git commit --verbose``
__ https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--v

``git-conflict-markers``
------------------------

A lexer for the conflict markers that Git adds to indicate conflicts during a merge.
All other text in the file is lexed as plain text.

``git-console``
---------------

A lexer for interactive shell sessions with Git.
It calls out to |BashLexer|__ for highlighting commands on lines starting with a ``$`` and |DiffLexer2|__ for highlighting inline diffs.

.. |BashLexer| replace:: ``BashLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.shell.BashLexer

.. |DiffLexer2| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer

``git-ignore``
--------------

A lexer for |.gitignore files|__.

.. |.gitignore files| replace:: ``.gitignore`` files
__ https://git-scm.com/docs/gitignore

``git-rebase-todo``
-------------------

A lexer for the ``git-rebase-todo`` file that Git opens when you run |git rebase --interactive|__.
It calls out to |BashLexer2|__ for highlighting commands on lines starting with ``x`` or ``exerc`` a ``$`` and |DiffLexer3|__ for highlighting inline diffs.

.. |git rebase --interactive| replace:: ``git rebase --interactive``
__ https://git-scm.com/docs/git-rebase#Documentation/git-rebase.txt--i

.. |BashLexer2| replace:: ``BashLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.shell.BashLexer

.. |DiffLexer3| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer
