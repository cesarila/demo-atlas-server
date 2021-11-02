import pytest, json
from flask import url_for, jsonify
from app.api import atlas
from app.models import Player
from app.services import p2sr
from app import api
from .conftest import generate_test_player


@pytest.mark.usefixtures('mocked_newname')
class TestHappyPaths:

    def test_get_valid_player_returns_200(self, db_session, client):
        testPlayer = generate_test_player(db_session)
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        assert response.status_code == 200

    def test_get_valid_player_returns_correct_name(self, db_session, client):
        testPlayer = generate_test_player(db_session)
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        response_json = json.loads(response.data.decode().strip())
        assert response_json == testPlayer.to_json()

    def test_get_expired_player_returns_200(self, db_session, client, force_update_condition):
        testPlayer = generate_test_player(db_session)
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        assert response.status_code == 200

    def test_get_expired_player_returns_fresh_name(self, db_session, client, force_update_condition):
        testPlayer = generate_test_player(db_session)
        original_json = testPlayer.to_json()
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        response_json = json.loads(response.data.decode().strip())
        assert original_json != response_json
        assert response_json == testPlayer.to_json()


class TestErrorResponses:

    def test_get_expired_player_while_p2sr_down_returns_502(self, db_session, client, mocked_p2sr_down, force_update_condition):
        testPlayer = generate_test_player(db_session)
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        assert response.status_code == 502

    def test_get_invalid_player_returns_404(self, db_session, client, mocked_player_does_not_exist):
        testPlayer = generate_test_player()
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        assert response.status_code == 404

    def test_update_player_after_p2sr_breaking_change_returns_500(self, db_session, client, mocked_p2sr_breaking_api_change, force_update_condition):
        testPlayer = generate_test_player(db_session)
        response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
        assert response.status_code == 500