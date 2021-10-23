# import json, requests
# from datetime import datetime
from app.models import Player
from app import db
from app.services import p2sr, time
from globals import *

def get_fresh_player(steam_id=-1):
    player = get_db_player(steam_id)
    if not player:
        display_name = p2sr.get_display_name(steam_id)
        if display_name:
            create_player(steam_id, display_name)
            player = get_db_player(steam_id)
        else:
            return None
    time_since_update = time.utc_now() - player.last_updated
    if time_since_update > MINIMUM_TIME_BEFORE_UPDATE:
        update_player(steam_id)
    return player

def create_player(steam_id, display_name):
    player = Player(steam_id=steam_id, display_name=display_name)
    db.session.add(player)
    db.session.commit()

def update_player(steam_id):
    player = Player.query.filter_by(steam_id=steam_id).first()
    player.display_name = p2sr.get_display_name(steam_id)
    db.session.commit()

def get_db_player(steam_id):
    return Player.query.filter_by(steam_id=steam_id).first()