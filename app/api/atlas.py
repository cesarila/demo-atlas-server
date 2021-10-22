import json, requests
from datetime import datetime
from flask import Blueprint, jsonify
from app.models import Player
from . import api
from app import db
from app.services import p2sr, time
from app.controllers import player_controller
from globals import *

@api.route('/<int:steam_id>', methods=['GET'])
def get_player_name(steam_id=-1):
    # player = get_player(steam_id)
    # if not player:
    #     display_name = p2sr.get_display_name(steam_id)
    #     if display_name:
    #         create_player(steam_id, display_name)
    #         player = get_player(steam_id)
    #         player = player.query.get()
    # time_since_update = time.utc_now() - player.last_updated
    # if time_since_update.total_seconds() > MINIMUM_TIME_BEFORE_UPDATE:
    #     update_player(steam_id)
    # response = jsonify(player.to_json())
    player = player_controller.get_fresh_player(steam_id)
    if player:
        response = jsonify(player.to_json())
        response.status_code = 200
        return response
    #TODO: Return Error Code

# def create_player(steam_id, display_name):
#     player = Player(steam_id=steam_id, display_name=display_name)
#     db.session.add(player)
#     db.session.commit()

# def update_player(steam_id):
#     player = Player.query.filter_by(steam_id=steam_id).first()
#     player.display_name = p2sr.get_display_name(steam_id)
#     db.session.commit()

# def get_player(steam_id):
#     return Player.query.filter_by(steam_id=steam_id).first()
