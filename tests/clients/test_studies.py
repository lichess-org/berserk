import pytest

from berserk import Client
from typing import List, Dict, Any, Iterator, Generator
from utils import validate, skip_if_older_3_dot_10

from berserk.types.studies import ChapterIdName


class TestLichessGames:
    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_export(self):
        res = Client().studies.export("Vl9LYHvz")
        validate(Iterator[str], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_export_chapter(self):
        res = Client().studies.export_chapter("Vl9LYHvz", "SruboJ1x")
        validate(str, res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_export_by_username(self):
        res = Client().studies.export_by_username("Chess700800")
        validate(Iterator[str], res)

    @skip_if_older_3_dot_10
    @pytest.mark.vcr
    def test_get_metadata_by_username(self):
        res = Client().studies.get_metadata_by_username("Chess700800")
        validate(List[Dict[str, Any]], res)
