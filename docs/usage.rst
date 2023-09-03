=====
Usage
=====

Use ``berserk`` by creating an API client:

.. code-block:: python

    >>> import berserk
    >>> client = berserk.Client()

Authenticating
==============

By default the client does not perform any authentication. However many of the
endpoints are not open. To use a form of authentication, just pass the
appropriate ``requests.Session``-like object:

- using an API token: ``berserk.TokenSession``
- using oauth: ``requests_oauthlib.Oauth2Session``

.. note::

    Some endpoints require specific Oauth2 permissions.

Using an API token
------------------

If you have a personal API token, you can simply use the ``TokenSession``
provided. For example, assuming you have written your token to
``'./lichess.token'``:

.. code-block:: python

    >>> with open('./lichess.token') as f:
    ...     token = f.read()
    ...
    >>> session = berserk.TokenSession(token)
    >>> client = berserk.Client(session)

Using Oauth2
------------

Some of the endpoints require OAuth2 authentication. Although outside the
scope of this documentation, you can use ``requests_oauthlib.Oauth2Session``
for this.

.. code-block:: python

    >>> from requests_oauthlib import OAuth2Session
    >>> session = OAuth2Session(...)
    >>> client = berserk.Client(session)


Accounts
========

Information and Preferences
---------------------------

.. code-block:: python

    >>> client.account.get()
    {'blocking': False,
     'count': {...},
     'createdAt': datetime.datetime(2018, 5, 16, 8, 9, 18, 187000),
     'followable': True,
     'following': False,
     'followsYou': False,
     'id': 'rhgrant10',
     'nbFollowers': 1,
     'nbFollowing': 1,
     'online': True,
     'perfs': {...},
     'playTime': {...},
     'seenAt': datetime.datetime(2018, 12, 9, 10, 28, 30, 221000),
     'url': 'https://lichess.org/@/rhgrant10',
     'username': 'rhgrant10'}

    >>> client.account.get_email()
    'rhgrant10@gmail.com'

    >>> client.account.get_preferences()
    {'animation': 2,
     'autoQueen': 1,
     ...
     'transp': False,
     'zen': 0}}

Kid Mode
--------

Using Oauth2, you can set the kid mode.

.. code-block:: python

    >>> client.account.set_kid_mode(True)  # enable
    True
    >>> client.account.set_kid_mode(False)  # disable
    True

Note that the ``set_kid_mode`` method returns an indicator of success and *not*
the current or previous status.

.. code-block:: python

    >>> def show_kid_mode():
    ...     is_enabled = client.account.get_kid_mode()
    ...     print('enabled' if is_enabled else 'disabled')
    ...
    >>> show_kid_mode()
    disabled

    >>> # try to enable, but the request fails
    >>> client.account.set_kid_mode(True)
    False
    >>> show_kid_mode()
    disabled

    >>> # try again, this time it succeeds
    >>> client.account.set_kid_mode(True)
    True
    >>> show_kid_mode()
    enabled

Bot Account Upgrade
-------------------

If this is a new account that has not yet played a game, and if you
have the required OAuth2 permission, you can upgrade the account to a bot
account:

.. code-block:: python

    >>> client.account.upgrade_to_bot()

Read more below about how to use bot functionality.


Users and Teams
===============

Realtime Statuses
-----------------

Get realtime information about one or more players:

.. code-block:: python

    >>> players = ['Sasageyo', 'Voinikonis_Nikita', 'Zugzwangerz', 'DOES-NOT-EXIST']
    >>> client.users.get_realtime_statuses(*players)
    [{'id': 'sasageyo',
    'name': 'Sasageyo',
    'title': 'IM',
    'online': True,
    'playing': True},
    {'id': 'voinikonis_nikita',
    'name': 'Voinikonis_Nikita',
    'title': 'FM',
    'online': True,
    'playing': True},
    {'id': 'zugzwangerz', 'name': 'Zugzwangerz'}]

Top 10 Lists
------------

.. code-block:: python

    >>> top10 = client.users.get_all_top_10()
    >>> list(top10)
    ['bullet',
     'blitz',
     'rapid',
     'classical',
     'ultraBullet',
     'crazyhouse',
     'chess960',
     'kingOfTheHill',
     'threeCheck',
     'antichess',
     'atomic',
     'horde',
     'racingKings']
    >>> top10['horde'][0]
    {'id': 'ingrid-vengeance',
     'perfs': {'horde': {'progress': 22, 'rating': 2443}},
     'username': 'Ingrid-Vengeance'}

Leaderboards
------------

.. code-block:: python

    >>> client.users.get_leaderboard('horde', count=11)[-1]
    {'id': 'philippesaner',
     'perfs': {'horde': {'progress': 10, 'rating': 2230}},
     'username': 'PhilippeSaner'}

Public Data
-----------

.. code-block:: python

    >>> client.users.get_public_data('PhilippeSaner')
    {'completionRate': 87,
     'count': {...},
     'createdAt': datetime.datetime(2017, 1, 9, 16, 14, 31, 140000),
     'id': 'philippesaner',
     'nbFollowers': 40,
     'nbFollowing': 13,
     'online': False,
     'perfs': {...},
     'playTime': {'total': 1505020, 'tv': 1038007},
     'profile': {'country': 'CA', 'location': 'Ottawa'},
     'seenAt': datetime.datetime(2018, 12, 9, 10, 26, 28, 22000),
     'url': 'https://lichess.org/@/PhilippeSaner',
     'username': 'PhilippeSaner'}

Activity Feeds
--------------

.. code-block:: python

    >>> feed = client.users.get_activity_feed('PhilippeSaner')
    >>> feed[0]
    {'games': {'horde': {'draw': 0,
       'loss': 1,
       'rp': {'after': 2230, 'before': 2198},
       'win': 12}},
     'interval': {'end': datetime.datetime(2018, 12, 9, 16, 0),
      'start': datetime.datetime(2018, 12, 8, 16, 0)},
     'tournaments': {'best': [{'nbGames': 1,
        'rank': 6,
        'rankPercent': 33,
        'score': 2,
        'tournament': {'id': '9zm2uIdP', 'name': 'Daily Horde Arena'}}],
      'nb': 1}}

Team Members
------------

.. code-block:: python

    >>> client.users.get_by_team('coders')
    <map at 0x107c1acc0>
    >>> members = list(_)
    >>> len(members)
    228

Live Streamers
--------------

.. code-block:: python

    >>> client.users.get_live_streamers()
    [{'id': 'chesspatzerwal', 'name': 'ChesspatzerWAL', 'patron': True},
     {'id': 'ayrtontwigg', 'name': 'AyrtonTwigg', 'playing': True},
     {'id': 'fanatikchess', 'name': 'FanatikChess', 'patron': True},
     {'id': 'jwizzy74', 'name': 'Jwizzy74', 'patron': True, 'playing': True},
     {'id': 'devjamesb', 'name': 'DevJamesB', 'playing': True},
     {'id': 'kafka4x', 'name': 'Kafka4x', 'playing': True},
     {'id': 'sparklehorse', 'name': 'Sparklehorse', 'patron': True, 'title': 'IM'},
     {'id': 'ivarcode', 'name': 'ivarcode', 'playing': True},
     {'id': 'pepellou', 'name': 'pepellou', 'patron': True, 'playing': True},
     {'id': 'videogamepianist', 'name': 'VideoGamePianist', 'playing': True}]


Exporting Games
===============

By Player
---------

Finished games can be exported and current games can be listed. Let's take a
look at the most recent 300 games played by "LeelaChess" on Dec. 8th, 2018:

.. code-block:: python

    >>> start = berserk.utils.to_millis(datetime(2018, 12, 8))
    >>> end = berserk.utils.to_millis(datetime(2018, 12, 9))
    >>> client.games.export_by_player('LeelaChess', since=start, until=end,
                                      max=300))
    <generator object Games.export_by_player at 0x10c24b048>
    >>> games = list(_)
    >>> games[0]['createdAt']
    datetime.datetime(2018, 12, 9, 22, 54, 24, 195000, tzinfo=datetime.timezone.utc)
    >>> games[-1]['createdAt']
    datetime.datetime(2018, 12, 8, 9, 11, 42, 229000, tzinfo=datetime.timezone.utc)

Wow, they play a lot of chess :)

By ID
-----

You can export games too using their IDs. Let's export the last game LeelaChess
played that day:

.. code-block:: python

    >>> game_id = games[0]['id']
    >>> client.games.export(game_id)
    {'analysis': [...],
     'clock': {'increment': 8, 'initial': 300, 'totalTime': 620},
     'createdAt': datetime.datetime(2018, 12, 9, 22, 54, 24, 195000, tzinfo=datetime.timezone.utc),
     'id': 'WatQhhbJ',
     'lastMoveAt': datetime.datetime(2018, 12, 9, 23, 5, 59, 396000, tzinfo=datetime.timezone.utc),
     'moves': ...
     'opening': {'eco': 'D38',
      'name': "Queen's Gambit Declined: Ragozin Defense",
      'ply': 8},
     'perf': 'rapid',
     'players': {'black': {'analysis': {'acpl': 44,
        'blunder': 1,
        'inaccuracy': 4,
        'mistake': 2},
       'rating': 1333,
       'ratingDiff': 0,
       'user': {'id': 'fsoto', 'name': 'fsoto'}},
      'white': {'analysis': {'acpl': 11,
        'blunder': 0,
        'inaccuracy': 2,
        'mistake': 0},
       'provisional': True,
       'rating': 2490,
       'ratingDiff': 0,
       'user': {'id': 'leelachess', 'name': 'LeelaChess', 'title': 'BOT'}}},
     'rated': True,
     'speed': 'rapid',
     'status': 'mate',
     'variant': 'standard',
     'winner': 'white'}

PGN vs JSON
-----------

Of course sometimes PGN format is desirable. Just pass ``as_pgn=True`` to
any of the export methods:

.. code-block:: python

    >>> pgn = client.games.export(game_id, as_pgn=True)
    >>> print(pgn)
    [Event "Rated Rapid game"]
    [Site "https://lichess.org/WatQhhbJ"]
    [Date "2018.12.09"]
    [Round "-"]
    [White "LeelaChess"]
    [Black "fsoto"]
    [Result "1-0"]
    [UTCDate "2018.12.09"]
    [UTCTime "22:54:24"]
    [WhiteElo "2490"]
    [BlackElo "1333"]
    [WhiteRatingDiff "+0"]
    [BlackRatingDiff "+0"]
    [WhiteTitle "BOT"]
    [Variant "Standard"]
    [TimeControl "300+8"]
    [ECO "D38"]
    [Opening "Queen's Gambit Declined: Ragozin Defense"]
    [Termination "Normal"]

    1. d4 { [%eval 0.08] [%clk 0:05:00] } 1... d5 ...

TV Channels
-----------

.. code-block:: python

    >>> channels = client.games.get_tv_channels()
    >>> list(channels)
    ['Bot',
     'Blitz',
     'Racing Kings',
     'UltraBullet',
     'Bullet',
     'Classical',
     'Three-check',
     'Antichess',
     'Computer',
     'Horde',
     'Rapid',
     'Atomic',
     'Crazyhouse',
     'Chess960',
     'King of the Hill',
     'Top Rated']
    >>> channels['King of the Hill']
    {'gameId': 'YPL6tP2K',
     'rating': 1554,
     'user': {'id': 'linischoki', 'name': 'linischoki'}}


Working with tournaments
========================

You have to specify the clock time, increment, and minutes, but creating a new
tournament is easy:

.. code-block:: python

    >>> client.tournaments.create_arena(clock_time=10, clock_increment=3, minutes=180)
    {'berserkable': True,
     'clock': {'increment': 3, 'limit': 600},
     'createdBy': 'rhgrant10',
     'duels': [],
     'fullName': "O'Kelly Arena",
     'greatPlayer': {'name': "O'Kelly",
      'url': "https://wikipedia.org/wiki/Alb%C3%A9ric_O'Kelly_de_Galway"},
     'id': '3uwyXjiC',
     'minutes': 180,
     'nbPlayers': 0,
     'perf': {'icon': '#', 'name': 'Rapid'},
     'quote': {'author': 'Bent Larsen',
      'text': 'I often play a move I know how to refute.'},
     'secondsToStart': 300,
     'standing': {'page': 1, 'players': []},
     'startsAt': '2018-12-10T00:32:12.116Z',
     'system': 'arena',
     'variant': 'standard',
     'verdicts': {'accepted': True, 'list': []}}

You can also create Swiss tournaments easily, specifying the team id, clock time,
clock increment, and number of rounds.

.. code-block:: python

    >>> client.tournaments.create_swiss(teamid_="coders", clock_limit=10,
                                        clock_increment=0, nbRounds=5)
    {'rated': true,
     'clock': {'increment': 0, 'limit': 600},
     'createdBy': "zccze",
     'greatPlayer': {'name': "Wang',
       'url':'https://wikipedia.org/wiki/Wang_Hao_(chess_player)' },
      'id': '3uwyXjiC'
      'name': 'Wang',
      'nbOngoing': 0,
      'nbPlayers': 0,
      'nbRounds': 5,
      'nextRound': { 'at': '2021-05-18T12:23:18.233-06:00', 'in': 600},
      'quote': {'author': 'Bent Larsen',
        'text': 'I often play a move I know how to refute.'},
      'round': 0,
      'startsAt': '2021-05-18T12:23:18.233-06:00',
      'status': 'created',
      'variant': 'standard'
      }

Additionally you can see tournaments that have recently finished, are in
progress, and are about to start:

.. code-block:: python

    >>> tournaments = client.tournaments.get()
    >>> list(tournaments)
    ['created', 'started', 'finished']
    >>> len(tournaments['created'])
    19
    >>> tournaments['created'][0]
    {'clock': {'increment': 0, 'limit': 300},
     'createdBy': 'bashkimneziri',
     'finishesAt': datetime.datetime(2018, 12, 24, 0, 21, 2, 179000, tzinfo=datetime.timezone.utc),
     'fullName': 'GM Arena',
     'id': 'COnVgmKH',
     'minutes': 45,
     'nbPlayers': 1,
     'perf': {'icon': ')', 'key': 'blitz', 'name': 'Blitz', 'position': 1},
     'rated': True,
     'secondsToStart': 160,
     'startsAt': datetime.datetime(2018, 12, 23, 23, 36, 2, 179000, tzinfo=datetime.timezone.utc),
     'status': 10,
     'system': 'arena',
     'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'},
     'winner': None}


Being a bot
===========

.. warning::

    These commands only work using bot accounts. Make sure you have converted
    the account with which you authenticate into a bot account first. See
    above for details.

Bots stream game information and react by calling various endpoints. There are
two streams of information:

1. incoming events
2. state of a particular game

In general, a bot will listen to the stream of incoming events, determine which
challenges to accept, and once accepted, listen to the stream of game states
and respond with the best moves in an attempt to win as many games as possible.
You *can* create a bot that looses intentionally if that makes you happy, but
regardless you will need to listen to both streams of information.

The typical pattern is to have one main thread that listens to the event
stream and spawns new threads when accepting challenges. Each challenge thread
then listens to the stream of state for that particular game and plays it to
completion.

Responding to challenges
------------------------

Here the goal is to respond to challenges and spawn workers to play those
accepted. Here's a bit of sample code that hits the highlights:

.. code-block:: python

    >>> is_polite = True
    >>> for event in client.bots.stream_incoming_events():
    ...     if event['type'] == 'challenge':
    ...         if should_accept(event):
    ...             client.bots.accept_challenge(event['id'])
    ...         elif is_polite:
    ...             client.bots.decline_challenge(event['id'])
    ...     elif event['type'] == 'gameStart':
    ...         game = Game(event['id'])
    ...         game.start()
    ...

Playing a game
--------------

Having accepted a challenge and recieved the gameStart event for it, the main
job here is to listen and react to the stream of the game state:

.. code-block:: python

    >>> class Game(threading.Thread):
    ...     def __init__(self, client, game_id, **kwargs):
    ...         super().__init__(**kwargs)
    ...         self.game_id = game_id
    ...         self.client = client
    ...         self.stream = client.bots.stream_game_state(game_id)
    ...         self.current_state = next(self.stream)
    ...
    ...     def run(self):
    ...         for event in self.stream:
    ...             if event['type'] == 'gameState':
    ...                 self.handle_state_change(event)
    ...             elif event['type'] == 'chatLine':
    ...                 self.handle_chat_line(event)
    ...
    ...     def handle_state_change(self, game_state):
    ...         pass
    ...
    ...     def handle_chat_line(self, chat_line):
    ...         pass
    ...

Obviously the code above is just to communicate the gist of what is required.
But once you have your framework for reacting to changes in game state, there
are a variety of actions you can take:

.. code-block:: python

    >>> client.bots.make_move(game_id, 'e2e4')
    True
    >>> client.bots.abort_game(game_id)
    True
    >>> client.bots.resign_game(game_id)
    True
    >>> client.bots.post_message(game_id, 'Prepare to loose')
    True
