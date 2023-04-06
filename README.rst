============
pygments-git
============

.. image:: https://img.shields.io/github/actions/workflow/status/adamchainz/pygments-git/main.yml?branch=main&style=for-the-badge
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

Installation
============

Use **pip**:

.. code-block:: sh

    python -m pip install pygments-git

Python 3.7 to 3.11 supported.

----

**Working on a Django project?**
Improve your skills with `one of my books <https://adamj.eu/books/>`__.

----

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

``git-commit-edit-msg``
-----------------------

A lexer for the ``COMMIT_EDITMSG`` file that Git opens when you run ``git commit``.
It calls out to |DiffLexer|__ for highlighting any diff, as added by |git commit --verbose|__.

.. |DiffLexer| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer

.. |git commit --verbose| replace:: ``git commit --verbose``
__ https://git-scm.com/docs/git-commit#Documentation/git-commit.txt--v

``git-console``
---------------

A lexer for interactive shell sessions with Git.
It calls out to |BashLexer|__ for highlighting commands on lines starting with a ``$`` and |DiffLexer2|__ for highlighting inline diffs.

.. |BashLexer| replace:: ``BashLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.shell.BashLexer

.. |DiffLexer2| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer

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
