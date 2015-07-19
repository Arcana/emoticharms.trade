from app import db


class Pack(db.Model):
    """ It's a pack mate. It contains 3 charms. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    charms = db.relationship('Charm', backref=db.backref('pack', lazy="joined"), lazy="joined")


class Charm(db.Model):
    """ It's a charm mate. Packs contain 3 of them. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pack_id = db.Column(db.Integer, db.ForeignKey("pack.id"))
    name = db.Column(db.String(128))
    hero = db.Column(db.String(128))