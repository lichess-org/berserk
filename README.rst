berserk
=======

.. image:: https://github.com/lichess-org/berserk/actions/workflows/test.yml/badge.svg
    :target: https://github.com/lichess-org/berserk/actions
    :alt: Test status

.. image:: https://badge.fury.io/py/berserk.svg
    :target: https://pypi.org/project/berserk/
    :alt: PyPI package

.. image:: https://github.com/lichess-org/berserk/actions/workflows/docs.yml/badge.svg
    :target: https://lichess-org.github.io/berserk/
    :alt: Docs

.. image:: https://img.shields.io/discord/280713822073913354.svg?label=discord&color=green&logo=discord
    :target: https://discord.gg/lichess
    :alt: Discord

Python client for the `Lichess API <https://lichess.org/api>`_.

This is based on the `original berserk version created by rhgrant10 <https://github.com/rhgrant10/berserk>`_ and the `berserk-downstream fork created by ZackClements <https://github.com/ZackClements/berserk>`_. Big thanks to them and all other contributors!

`Documentation <https://lichess-org.github.io/berserk/>`_

Installation
------------

Requires Python 3.8+. Download and install the latest release:
::

    pip3 install berserk

If you have `berserk-downstream` installed, make sure to uninstall it first!

Features
--------

* handles (ND)JSON and PGN formats at user's discretion
* token auth session
* easy integration with OAuth2
* automatically converts time values to datetimes

Usage
-----

You can use any ``requests.Session``-like object as a session, including those
from ``requests_oauth``. A simple token session is included, as shown below:

.. code:: python

    import berserk

    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)


Most of the API is available:

.. code:: python

    client.account.get
    client.account.get_email
    client.account.get_preferences
    client.account.get_kid_mode
    client.account.set_kid_mode
    client.account.upgrade_to_bot

    client.board.stream_incoming_events
    client.board.seek
    client.board.stream_game_state
    client.board.make_move
    client.board.post_message
    client.board.get_game_chat
    client.board.abort_game
    client.board.resign_game
    client.board.handle_draw_offer
    client.board.offer_draw
    client.board.accept_draw
    client.board.decline_draw
    client.board.handle_takeback_offer
    client.board.offer_takeback
    client.board.accept_takeback
    client.board.decline_takeback
    client.board.claim_victory
    client.board.go_berserk

    client.bots.get_online_bots
    client.bots.stream_incoming_events
    client.bots.stream_game_state
    client.bots.make_move
    client.bots.post_message
    client.bots.abort_game
    client.bots.resign_game
    client.bots.accept_challenge
    client.bots.decline_challenge

    client.broadcasts.get_official
    client.broadcasts.create
    client.broadcasts.get
    client.broadcasts.update
    client.broadcasts.push_pgn_update
    client.broadcasts.create_round
    client.broadcasts.get_round
    client.broadcasts.update_round
    client.broadcasts.get_round_pgns
    client.broadcasts.get_pgns

    client.challenges.create
    client.challenges.create_ai
    client.challenges.create_open
    client.challenges.create_with_accept
    client.challenges.accept
    client.challenges.decline

    client.games.export
    client.games.export_ongoing_by_player
    client.games.export_by_player
    client.games.export_multi
    client.games.get_among_players
    client.games.stream_games_by_ids
    client.games.add_game_ids_to_stream
    client.games.get_ongoing
    client.games.stream_game_moves
    client.games.get_tv_channels
    client.games.import_game

    client.messaging.send

    client.oauth.test_tokens

    client.puzzles.get_daily
    client.puzzles.get
    client.puzzles.get_puzzle_activity
    client.puzzles.get_puzzle_dashboard
    client.puzzles.get_storm_dashboard

    client.relations.get_users_followed
    client.relations.follow
    client.relations.unfollow

    client.simuls.get

    client.studies.export_chapter
    client.studies.export

    client.tablebase.look_up
    client.tablebase.standard
    client.tablebase.atomic
    client.tablebase.antichess

    client.teams.get_members
    client.teams.join
    client.teams.leave
    client.teams.kick_member

    client.tournaments.get
    client.tournaments.get_tournament
    client.tournaments.create_arena
    client.tournaments.create_swiss
    client.tournaments.export_arena_games
    client.tournaments.export_swiss_games
    client.tournaments.arena_by_team
    client.tournaments.swiss_by_team
    client.tournaments.tournaments_by_user
    client.tournaments.stream_results
    client.tournaments.stream_by_creator

    client.tv.get_current_games
    client.tv.stream_current_game
    client.tv.get_best_ongoing

    client.users.get_realtime_statuses
    client.users.get_all_top_10
    client.users.get_leaderboard
    client.users.get_public_data
    client.users.get_activity_feed
    client.users.get_by_id
    client.users.get_by_team
    client.users.get_live_streamers
    client.users.get_rating_history
    client.users.get_crosstable
    client.users.get_user_performance

Details for each function can be found in the `documentation <https://lichess-org.github.io/berserk/>`_.
