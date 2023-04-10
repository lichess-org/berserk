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

Users
-----

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

Relations
---------

- Get users followed by the logged in user
- Follow a player
- Unfollow a player

Teams
-----

- Get members of a team
- Join a team
- Leave a team
- Kick a user from your team

Games
-----

TO-DO
=====

Users
-----

- Autocomplete usernames

Teams
-----

- Get team swiss tournaments
- Get a single team
- Get popular teams
- Teams of a player
- Search teams
- Get team Arena tournaments
- Get join requests
- Accept join request
- Decline join request
- Message all members
