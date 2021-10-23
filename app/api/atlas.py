from flask import jsonify
from . import api
from app.controllers import player_controller
from app.services import time, p2sr, extract_display_name, is_ok
from globals import *

@api.route('/<int:steam_id>', methods=['GET'])
def get_player_name(steam_id=-1):
    player = player_controller.get_db_player(steam_id)
    if not player:
        response = p2sr.get_display_name(steam_id)
        return process_p2sr_response(player_controller.create_player, steam_id)
    time_since_update = time.utc_now() - player.last_updated
    if time_since_update > MINIMUM_TIME_BEFORE_UPDATE:
        return process_p2sr_response(player_controller.update_player, steam_id)
    response = jsonify(player.to_json())
    response.status_code = 200
    return response

def process_p2sr_response(player_controller_function, steam_id):
    response = p2sr.get_display_name(steam_id)
    if is_ok(response):
        player_controller_function(steam_id, extract_display_name(response))
    return response