=========
Changelog
=========

Unreleased
----------

* Support Python 3.15.

* Switch package build backend from setuptools to `uv_build <https://docs.astral.sh/uv/concepts/build-backend/>`__.
  This makes builds with uv about nine times faster, since uv runs the backend natively, without creating a build environment or spawning a Python process.
  Additionally, source distributions no longer include test files, which setuptools previously included incompletely, missing the files needed to actually run them.

* Drop Python 3.9 support.

1.9.0 (2025-09-09)
------------------

* Support Python 3.14.

1.8.0 (2024-10-23)
------------------

* Drop Python 3.8 support.

* Support Python 3.13.

1.7.0 (2023-08-30)
------------------

* Add ``git-blame-ignore-revs`` lexer.

1.6.0 (2023-07-10)
------------------

* Drop Python 3.7 support.

1.5.0 (2023-06-16)
------------------

* Support Python 3.12.

1.4.1 (2023-05-31)
------------------

* Fix ``git-conflict-markers`` highlighting of non-marker lines that use marker symbols.

1.4.0 (2023-05-24)
------------------

* Support hint, error, and fatal lines in ``git-console``.

* Fix ``commit`` lines and support ``Merge:`` lines in ``git-console``.

1.3.0 (2023-04-17)
------------------

* Add ``git-ignore`` lexer.

1.2.0 (2023-04-16)
------------------

* Add ``git-attributes`` and ``git-conflict-markers`` lexers.

1.1.0 (2023-04-06)
------------------

* Add ``git-commit-edit-msg`` and ``git-rebase-todo`` lexers.

* Improve ``git-console``: handle more ``git log`` outputs, and highlight results from ``git commit``.

1.0.0 (2023-04-04)
------------------

* First release.
