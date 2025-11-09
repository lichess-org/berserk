import pytest
from berserk import Client


class TestRelations:
    """Tests for Relations client."""

    @pytest.mark.vcr
    def test_follow(self):
        """Test following a user."""
        Client().relations.follow("lichess")

    @pytest.mark.vcr
    def test_unfollow(self):
        """Test unfollowing a user."""
        Client().relations.unfollow("lichess")

    @pytest.mark.vcr
    def test_block(self):
        """Test blocking a user."""
        Client().relations.block("lichess")

    @pytest.mark.vcr
    def test_unblock(self):
        """Test unblocking a user."""
        Client().relations.unblock("lichess")

    @pytest.mark.vcr
    def test_get_users_followed(self):
        """Test streaming users followed."""
        users_gen = Client().relations.get_users_followed()

        first_user = next(users_gen, None)

        if first_user:
            assert "id" in first_user
            assert "username" in first_user
