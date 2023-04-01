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

.. code-block:: console

    .. code-block:: git-console

        $ git log --oneline
        82fbbd3 D'oh! Fix math proof
        91e9879 Aye carumba! Grammar mistake
        61c4c08 Cowabunga! Update bibliography

``git-console``
---------------

A lexer for displaying interactive shell sessions with Git.
It calls out to |BashLexer|__ for highlighting commands on lines starting with a ``$`` and |DiffLexer|__ for highlighting inline diffs.

.. |BashLexer| replace:: ``BashLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.shell.BashLexer

.. |DiffLexer| replace:: ``DiffLexer``
__ https://pygments.org/docs/lexers/#pygments.lexers.diff.DiffLexer
