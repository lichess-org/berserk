.. highlight:: shell

Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/lichess-org/berserk/issues.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Make sure the feature is uncontroversial or that a maintainer has validated it before starting working on it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

berserk could always use more documentation, whether as part of the
official berserk docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/lichess-org/berserk/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

- Install ``poetry`` (``$ pip3 install poetry``)
- Setup dependencies by running ``$ poetry install --with dev``

For a PR to be merged, it needs to pass the CI, you can reproduce most of them locally (commands assume being in the root directory of this repo):
- To run tests use ``$ poetry run pytest``
- To check format use ``$ poetry run black .``
- To check doc generation use ``$ poetry run sphinx-build -b html docs _build -EW``


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in CHANGELOG.rst).
Then run::

$ TBD
