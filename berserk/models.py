from __future__ import annotations

from typing import Dict, List, Tuple, TypeVar, overload

from . import utils

T = TypeVar("T")


class model(type):
    @property
    def conversions(cls):
        return {k: v for k, v in vars(cls).items() if not k.startswith("_")}


class Model(metaclass=model):
    @overload
    @classmethod
    def convert(cls, data: Dict[str, T]) -> Dict[str, T]: ...

    @overload
    @classmethod
    def convert(
        cls, data: List[Dict[str, T]] | Tuple[Dict[str, T], ...]
    ) -> List[Dict[str, T]]: ...

    @classmethod
    def convert(
        cls, data: Dict[str, T] | List[Dict[str, T]] | Tuple[Dict[str, T], ...]
    ) -> Dict[str, T] | List[Dict[str, T]]:
        if isinstance(data, (list, tuple)):
            return [cls.convert_one(v) for v in data]
        return cls.convert_one(data)

    @classmethod
    def convert_one(cls, data: Dict[str, T]) -> Dict[str, T]:
        for k in set(data) & set(cls.conversions):
            data[k] = cls.conversions[k](data[k])
        return data

    @classmethod
    def convert_values(cls, data: Dict[str, Dict[str, T]]) -> Dict[str, Dict[str, T]]:
        for k in data:
            data[k] = cls.convert(data[k])
        return data


class Account(Model):
    createdAt = utils.datetime_from_millis
    seenAt = utils.datetime_from_millis


class User(Model):
    createdAt = utils.datetime_from_millis
    seenAt = utils.datetime_from_millis


class Activity(Model):
    interval = utils.inner(utils.datetime_from_millis, "start", "end")


class Game(Model):
    createdAt = utils.datetime_from_millis
    lastMoveAt = utils.datetime_from_millis


class GameState(Model):
    createdAt = utils.datetime_from_millis
    wtime = utils.timedelta_from_millis
    btime = utils.timedelta_from_millis
    winc = utils.timedelta_from_millis
    binc = utils.timedelta_from_millis


class Tournament(Model):
    startsAt = utils.datetime_from_str_or_millis


class Broadcast(Model):
    broadcast = utils.inner(utils.datetime_from_millis, "startedAt", "startsAt")


class RatingHistory(Model):
    points = utils.listing(utils.rating_history)


class PuzzleActivity(Model):
    date = utils.datetime_from_millis


class OAuth(Model):
    expires = utils.datetime_from_millis


class TV(Model):
    createdAt = utils.datetime_from_millis
    lastMoveAt = utils.datetime_from_millis
