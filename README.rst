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


Most of the API is available (in alphabetical order):

.. code:: python

    client.account.get
    client.account.get_email
    client.account.get_kid_mode
    client.account.get_preferences
    client.account.set_kid_mode
    client.account.upgrade_to_bot

    client.board.abort_game
    client.board.accept_draw
    client.board.accept_takeback
    client.board.claim_victory
    client.board.decline_draw
    client.board.decline_takeback
    client.board.get_game_chat
    client.board.go_berserk
    client.board.handle_draw_offer
    client.board.handle_takeback_offer
    client.board.make_move
    client.board.offer_draw
    client.board.offer_takeback
    client.board.post_message
    client.board.resign_game
    client.board.seek
    client.board.stream_game_state
    client.board.stream_incoming_events

    client.bots.abort_game
    client.bots.accept_challenge
    client.bots.decline_challenge
    client.bots.get_online_bots
    client.bots.make_move
    client.bots.post_message
    client.bots.resign_game
    client.bots.stream_game_state
    client.bots.stream_incoming_events

    client.broadcasts.create
    client.broadcasts.get
    client.broadcasts.push_pgn_update
    client.broadcasts.update

    client.challenges.accept
    client.challenges.create
    client.challenges.create_ai
    client.challenges.create_open
    client.challenges.create_with_accept
    client.challenges.decline

    client.games.add_game_ids_to_stream
    client.games.export
    client.games.export_by_player
    client.games.export_multi
    client.games.export_ongoing_by_player
    client.games.get_among_players
    client.games.get_ongoing
    client.games.get_tv_channels
    client.games.import_game
    client.games.stream_game_moves
    client.games.stream_games_by_ids

    client.messaging.send

    client.oauth.test_tokens

    client.relations.follow
    client.relations.get_users_followed
    client.relations.unfollow

    client.simuls.get

    client.studies.export
    client.studies.export_chapter

    client.teams.get_members
    client.teams.join
    client.teams.kick_member
    client.teams.leave

    client.tournaments.arena_by_team
    client.tournaments.create_arena
    client.tournaments.create_swiss
    client.tournaments.export_arena_games
    client.tournaments.export_swiss_games
    client.tournaments.get
    client.tournaments.get_tournament
    client.tournaments.stream_by_creator
    client.tournaments.stream_results
    client.tournaments.swiss_by_team
    client.tournaments.tournaments_by_user

    client.tv.get_best_ongoing
    client.tv.get_current_games
    client.tv.stream_current_game

    client.users.get_activity_feed
    client.users.get_all_top_10
    client.users.get_by_id
    client.users.get_by_team
    client.users.get_crosstable
    client.users.get_leaderboard
    client.users.get_live_streamers
    client.users.get_public_data
    client.users.get_puzzle_activity
    client.users.get_rating_history
    client.users.get_realtime_statuses
    client.users.get_user_performance

Details for each function can be found in the `documentation <https://lichess-org.github.io/berserk/>`_.
