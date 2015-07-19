from app.emoticharms.models import Pack
from flask_wtf import Form
from wtforms import IntegerField
from wtforms.form import FormMeta
from wtforms.validators import DataRequired


class UserPacksFormMeta(type):

    def __new__(cls, name, parents, dct):
        packs = Pack.query.all()
        for pack in packs:
            dct[pack.name] = IntegerField(pack.name, validators=[DataRequired()])
        return super(UserPacksFormMeta, cls).__new__(cls, name, parents, dct)


class CombinedUserPacksFormMeta(UserPacksFormMeta, FormMeta):
    pass


class UserPacksForm(Form):

    __metaclass__ = CombinedUserPacksFormMeta
