from app import db


class UserPack(db.Model):
    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.account_id'), primary_key=True)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    pack = db.relationship("Pack", backref="user_pack")
    user = db.relationship("User", backref="user_pack")

    def __init__(self, pack_id, user_id, quantity):
        self.pack_id = pack_id
        self.user_id = user_id
        self.quantity = quantity


class Pack(db.Model):
    """ It's a pack mate. It contains 3 charms. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    charms = db.relationship('Charm', backref=db.backref('pack', lazy="joined"), lazy="joined")

    @property
    def normalized_name(self):
        return self.name.lower().strip()


class Charm(db.Model):
    """ It's a charm mate. Packs contain 3 of them. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pack_id = db.Column(db.Integer, db.ForeignKey("pack.id"))
    name = db.Column(db.String(128))
    hero = db.Column(db.String(128))
    image = db.Column(db.String(16384))

    @property
    def image_url(self):
        return 'data:image/png;base64,' + self.image
