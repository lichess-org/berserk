.. role:: python(code)
   :language: python

======
Status
======

Done
====

Account
-------

- Get my profile
- Get my email adress
- Get my preferences
- Get my kid mode status
- Set my kid mode status

.. note::
    Also in accounts: :py:meth:`berserk.clients.Account.upgrade_to_bot`.

User
----

- Get real-time users status
- Get all top 10
- Get leaderboard
- Get user public data
    .. error::
        Missing ``trophies`` parameter.
- Get rating history of a user
- Get performance statistics
- Get user activity
- Get users by ID
- Get members of a team
    .. warning::
        Deprecated. Use :py:meth:`berserk.clients.Teams.get_members` instead.
- Get live streamers
- Get crosstable

.. note::
    Also in users: :py:meth:`berserk.clients.Users.get_puzzle_activity`

TO-DO
=====

Users
-----

- Autocomplete usernames
