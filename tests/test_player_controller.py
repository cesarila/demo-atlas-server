import pytest
from .conftest import generate_test_player
from app.models import Player
from app.controllers import player_controller


@pytest.mark.usefixtures('mocked_newname')
class TestHappyPath:
    def test_create_player(self, db_session):
        assert Player.query.count() == 0
        testPlayer = generate_test_player()
        player_controller.create_player(steam_id=testPlayer.steam_id, display_name=testPlayer.display_name)
        assert Player.query.count() == 1
        dbPlayer = Player.query.filter_by(steam_id=testPlayer.steam_id).first()
        assert dbPlayer.steam_id == testPlayer.steam_id
        assert dbPlayer.display_name == testPlayer.display_name
        assert dbPlayer.last_updated is not None


    def test_update_player(self, db_session):
        testPlayer = generate_test_player(db_session)
        player_controller.update_player(testPlayer.steam_id)
        assert testPlayer.display_name == 'verycoolupdatedname'


    def test_get_fresh_player_updates_after_threshold(self, db_session, client, force_update_condition):
        testPlayer = generate_test_player(db_session)
        player_controller.get_fresh_player(testPlayer.steam_id)

        dbPlayer = Player.query.filter_by(steam_id=testPlayer.steam_id).first()
        assert dbPlayer.display_name == 'verycoolupdatedname'