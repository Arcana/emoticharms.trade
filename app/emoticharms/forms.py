from app.emoticharms.models import Pack
from flask_wtf import Form
from sqlalchemy.orm import joinedload
from wtforms import IntegerField
from wtforms.form import FormMeta
from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import Input


class QuantityInput(Input):

    input_type = 'number'

    def __init__(self, pack, *args, **kwargs):
        self.pack = pack
        super(QuantityInput, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('min', 0)
        kwargs.setdefault('step', 1)
        input_tag = super(QuantityInput, self).__call__(field, **kwargs)
        return '<span>{0}{1}</span>'.format(self.image_tags, input_tag)

    @property
    def image_tags(self):
        return ''.join('<img class="charm" src="{0}"></img>'.format(charm.image_url) for charm in self.pack.charms)


class PackQuantityField(IntegerField):

    def __init__(self, pack, *args, **kwargs):
        assert isinstance(pack, Pack)
        self.pack = pack
        self.widget = QuantityInput(pack)
        super(PackQuantityField, self).__init__(*args, **kwargs)


class UserPacksFormMeta(type):

    def __new__(cls, name, parents, dct):
        packs = Pack.query.options(joinedload('charms')).all()
        for pack in packs:
            dct[pack.normalized_name] = PackQuantityField(
                pack,
                default=0,
                validators=[InputRequired(), NumberRange(min=0)],
            )
        return super(UserPacksFormMeta, cls).__new__(cls, name, parents, dct)


class CombinedUserPacksFormMeta(UserPacksFormMeta, FormMeta):
    pass


class UserPacksForm(Form):

    __metaclass__ = CombinedUserPacksFormMeta
