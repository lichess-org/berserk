Changelog
=========

v0.12.9 (2023-09-2)
-------------------

* Added ``client.bulk_pairings`` to create and manage bulk pairings
  * ``client.bulk_pairings.get_upcoming`` to get upcoming bulk pairings you created
  * ``client.bulk_pairings.create`` to create a bulk pairing
  * ``client.bulk_pairings.start_clocks`` to start the clocks of a bulk pairing
  * ``client.bulk_pairings.cancel`` to cancel a bulk pairing
* Added better return types for ``client.account.get`` and ``client.account.get_preferences``

Thanks to @Virinas-code for their contributions to this release.

v0.12.8 (2023-07-25)
--------------------

* Added ``client.opening_explorer.get_lichess_games`` to request opening explorer data for a given position based on Lichess games

Thanks to @rpesche for their contributions to this release.

v0.12.7 (2023-07-15)
--------------------

* Added ``client.teams.get_join_requests`` to get the join requests of one of your teams
* Added ``client.teams.accept_join_request`` to accept a join request of one of your teams

Thanks to @zen1405 for their contributions to this release.

v0.12.6 (2023-06-18)
--------------------

* Added ``client.puzzles.get_daily`` to get the current daily puzzle
* Added ``client.puzzles.get_puzzle_activity`` to get the authenticated user's puzzle activity/history

  * This was already accessibly as ``client.users.get_puzzle_activity`` and remains there for backwards compatibility but this usage is deprecated and will be removed in the next breaking version.

* Added ``client.puzzles.get_puzzle_dashboard`` to get the authenticated user's puzzle dashboard
* Added ``client.puzzles.get_storm_dashboard`` to get the storm dashboard of a user
* Added ``client.tablebase.look_up`` to look up tablebase results
* Added ``client.tablebase.standard`` to look up tablebase results
* Added ``client.tablebase.atomic`` to look up atomic chess tablebase results
* Added ``client.tablebase.antichess`` to look up antichess tablebase results

* All streaming methods are now generators which means they only start the request once the iteration starts. For most usages, this doesn't make any difference.

Thanks to @icp, @obazin, and @Virinas-code for their contributions to this release.

v0.12.5 (2023-06-15)
--------------------

* Added ``client.broadcast.get_official`` to get official Broadcasts
* Added ``client.broadcast.get_round_pgns`` to get the PGN of all games of a broadcast round
* Added ``client.broadcast.get_pgns`` to get the PGN of all games of a broadcast
* Added ``client.puzzles.get`` to get a puzzle by its id

Thanks to @obazin and @thegrapesoda for their contributions to this release.

v0.12.4 (2023-05-21)
--------------------

* Fixed ``client.users.get_puzzle_activity`` returning 404 all the time.

Thanks to @AnonJohn for the report.

v0.12.3 (2023-05-16)
--------------------

* Fixed response handling of several endpoints related to datetime parsing for python older than 3.11

Thanks to @aro5000 for the report and @icp1994 for the troubleshooting.

v0.12.2 (2023-05-14)
--------------------

* Fixed response handling of several endpoints related to datetime parsing

Thanks to @icp1994 for their contributions to this release!

v0.12.1 (2023-05-13)
--------------------

* Added ``client.bots.get_online_bots`` to get the list of online bots
* Adjusted study export endpoint URLs to use the ``/api`` prefix for consistency

Thanks to @kalpgarg and @icp1994 for their contributions to this release!

v0.12.0 (2023-05-07)
--------------------

* First release done by Lichess incorporating the changes from ``berserk-downstream`` (v0.11.0)
* Added type hints
* Removed deprecated functions
* Added ``client.board.get_game_chat`` to get the chat of a game
* Added ``client.board.claim_victory`` to claim victory in a game (after the opponent left the game)
* Added ``client.board.go_berserk`` to go berserk in a tournament game
* ``export_arena_games`` and ``export_swiss_games`` now stream the result (i.e. return an iterator over the games)

Thanks to @trevorbayless and @icp1994 for their contributions to this release!


v0.11.0 (2021-03-18)
--------------------

* Added ``Tournaments.create_arena`` for creating arena tournaments
* Added ``Tournaments.create_swiss`` for creating swiss tournaments
* Added ``Tournaments.export_arena_games`` for exporting arena games
* Added ``Tournaments.export_swiss_games`` for exporting swiss games
* Added ``Tournaments.arena_by_team`` for getting arena tournaments by team
* Added ``Tournaments.swiss_by_team`` for getting swiss tournaments by team
* Added ``Tournaments.tournaments_by_user`` for getting tournaments by user
* Deprecated ``Tournaments.create`` and ``Tournaments.export_games``
* Uploaded fork to pypi
* Minor fixes for docstrings
* Minor updates to README, AUTHORS

v0.10.0 (2020-04-26)
--------------------

* Added ``Challenge.create_ai`` for creating an AI challenge
* Added ``Challenge.create_open`` for creating an open challenge
* Added ``Challenge.create_with_accept`` auto-acceptance of challenges using OAuth token
* Bugfix for passing initial board positions in FEN for challenges
* Minor fixes for docstrings

v0.9.0 (2020-04-14)
-------------------

* Added remaining ``Board`` endpoints: seek, handle_draw_offer, offer_draw, accept_draw, and decline_draw
* Multiple doc updates/fixes
* Added codecov reporting

v0.8.0 (2020-03-08)
-------------------

* Added new ``Board`` client: stream_incoming_events, stream_game_state, make_move, post_message, abort_game, and resign_game

v0.7.0 (2020-01-26)
-------------------

* Added simuls
* Added studies export and export chapter
* Added tournament results, games export, and list by creator
* Added user followers, users following, rating history, and puzzle activity
* Added new ``Teams`` client: join, get members, kick member, and leave
* Updated documentation, including new docs for some useful utils
* Fixed bugs in ``Tournaments.export_games``
* Deprecated ``Users.get_by_team`` - use ``Teams.get_members`` instead


v0.6.1 (2020-01-20)
-------------------

* Added py37 to the travis build
* Updated development status classifier to 4 - Beta
* Fixed py36 issue preventing successful build
* Made updates to the Makefile


v0.6.0 (2020-01-20)
-------------------

* Added logging to the ``berserk.session`` module
* Fixed exception message when no cause
* Fixed bug in ``Broadcasts.push_pgn_update``
* Updated documentation and tweak the theme


v0.5.0 (2020-01-20)
-------------------

* Added ``ResponseError`` for 4xx and 5xx responses with status code, reason, and cause
* Added ``ApiError`` for all other request errors
* Fixed test case broken by 0.4.0 release
* Put all utils code under test


v0.4.0 (2020-01-19)
-------------------

* Added support for the broadcast endpoints
* Added a utility for easily converting API objects into update params
* Fixe multiple bugs with the tournament create endpoint
* Improved the reusability of some conversion utilities
* Improved many docstrings in the client classes


v0.3.2 (2020-01-04)
-------------------

* Fixed bug where options not passed for challenge creation
* Converted requirements from pinned to sematically compatible
* Bumped all developer dependencies
* Use pytest instead of the older py.test
* Use py37 in tox


v0.3.1 (2018-12-23)
-------------------

* Converted datetime string in tournament creation response into datetime object


v0.3.0 (2018-12-23)
-------------------

* Converted all timestamps to datetime in all responses
* Provided support for challenging other players to a game


v0.2.1 (2018-12-08)
-------------------

* Bump edrequests dependency to >-2.20.0 (CVE-2018-18074)


v0.2.0 (2018-12-08)
-------------------

* Added `position` and `start_date` params to `Tournament.create`
* Added `Position` enum


v0.1.2 (2018-07-14)
-------------------

* Fixed an asine bug in the docs


v0.1.1 (2018-07-14)
-------------------

* Added tests for session and formats modules
* Fixed mispelled PgnHandler class (!)
* Fixed issue with trailing whitespace when splitting multiple PGN texts
* Fixed the usage overview in the README
* Fixed the versions for travis-ci
* Made it easier to test the `JsonHandler` class
* Salted the bumpversion config to taste


v0.1.0 (2018-07-10)
-------------------

* First release on PyPI.
