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

Implement Missing Endpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can run the ``check-endpoints.py`` script (requites yaml to be installed, ``pip3 install pyyaml``) in the root of the project to get a list of endpoints that are still missing.

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

- Install ``poetry`` (``pip3 install poetry``)
- Setup dependencies by running ``poetry install --with dev`` or ``make setup``
- Start editing the code
- To test your changes, run ``poetry shell`` to activate the poetry environment, open a python interpreter (``python3``), and import the library to test your changes::

    >>> import berserk
    >>> client = berserk.Client()
    >>> client.users.my_new_method()

For a PR to be merged, it needs to pass the CI, you can reproduce most of them locally (commands assume being in the root directory of this repo):

- To run tests use ``poetry run pytest`` or ``make test``
- To check format use ``poetry run black .`` or ``make format``
- To check doc generation use ``poetry run sphinx-build -b html docs _build -EW`` or ``make docs``

  - You can then open ``_build/index.html`` in your browser or use ``python3 -m http.server --directory _build`` to serve it locally
  - Alternatively, run ``make servedocs`` to automatically build and serve them on http://localhost:8000


Deploying
---------

A reminder for the maintainers on how to deploy.

You need a PyPI account with access to the ``berserk`` package and have an API token with the corresponding access configured for poetry (see https://python-poetry.org/docs/repositories/#configuring-credentials):

- Create a token: https://pypi.org/manage/account/token/ (you can see your existing tokens at https://pypi.org/manage/account/)
- Configure poetry: ``poetry config pypi-token.pypi <your-token>``. Add a space before the command to avoid it being saved in your shell history.

Make sure all your changes are committed (including an entry in CHANGELOG.rst) and you set the version in ``pyproject.toml`` correctly.

Then run ``poetry publish --build`` or ``make publish`` and tag the release on git: ``git tag v1.2.3 && git push --tags``
