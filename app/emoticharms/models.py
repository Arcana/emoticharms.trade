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

    @property
    def image_url(self):
        # FIXME
        return 'data:image/png;base64,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'
