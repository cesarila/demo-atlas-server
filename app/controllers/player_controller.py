from app.models import Player
from app import db

def create_player(steam_id, display_name):
    player = Player(steam_id=steam_id, display_name=display_name)
    db.session.add(player)
    db.session.commit()

def update_player(steam_id, display_name):
    player = Player.query.filter_by(steam_id=steam_id).first()
    player.display_name = display_name
    db.session.commit()

def get_db_player(steam_id):
    return Player.query.filter_by(steam_id=steam_id).first()