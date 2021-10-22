import pytest, json
from flask import url_for, jsonify
from app.api import atlas
from app.models import Player
from app.services import p2sr
from app import api
from .conftest import generate_test_player

def test_get_valid_player_returns_200(db_session, client, mocked_newname):
    testPlayer = generate_test_player(db_session)
    response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
    assert response.status_code == 200

def test_get_valid_player_returns_correct_name(db_session, client, mocked_newname):
    testPlayer = generate_test_player(db_session)
    response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
    response_json = json.loads(response.data.decode().strip())
    assert response_json == testPlayer.to_json()

def test_get_expired_player_returns_200(db_session, client, mocked_newname, force_update_condition):
    testPlayer = generate_test_player(db_session)
    response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
    assert response.status_code == 200

def test_get_expired_player_returns_fresh_name(db_session, client, mocked_newname, force_update_condition):
    testPlayer = generate_test_player(db_session)
    original_json = testPlayer.to_json()
    response = client.get(url_for('api.get_player_name', steam_id=testPlayer.steam_id))
    response_json = json.loads(response.data.decode().strip())
    assert original_json != response_json
    assert response_json == testPlayer.to_json()