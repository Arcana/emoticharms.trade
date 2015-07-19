from app import db


class UserPack(db.Model):
    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.account_id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    pack = db.relationship("Pack", backref="user_pack")
    user = db.relationship("User", backref="user_pack")


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
