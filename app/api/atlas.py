from flask import jsonify
from . import api
from app.controllers import player_controller

@api.route('/<int:steam_id>', methods=['GET'])
def get_player_name(steam_id=-1):
    player = player_controller.get_fresh_player(steam_id)
    if player:
        response = jsonify(player.to_json())
        response.status_code = 200
        return response
