from .. import db
from dbUtils import utcnow

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.BigInteger, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    last_updated = db.Column(db.DateTime, onupdate=utcnow(), server_default=utcnow())
    db.UniqueConstraint(steam_id)

    def __repr__(self):
        return '<Player %r>' % self.id

    def to_json(self):
        player_json = {
        'displayName': self.display_name
        }
        return player_json