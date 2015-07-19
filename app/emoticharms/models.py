from app import db


user_packs = db.Table('user_packs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.account_id'), nullable=False),
    db.Column('pack_id', db.Integer, db.ForeignKey('pack.id'), nullable=False),
    db.Column('quantity', db.Integer, nullable=False, server_default="0"),
)


class Pack(db.Model):
    """ It's a pack mate. It contains 3 charms. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    charms = db.relationship('Charm', backref=db.backref('pack', lazy="joined"), lazy="joined")
    users = db.relationship('User', secondary=user_packs,
        backref=db.backref('packs', lazy='dynamic'))


class Charm(db.Model):
    """ It's a charm mate. Packs contain 3 of them. """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pack_id = db.Column(db.Integer, db.ForeignKey("pack.id"))
    name = db.Column(db.String(128))
    hero = db.Column(db.String(128))
