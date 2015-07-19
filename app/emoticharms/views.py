from flask import Blueprint, flash, redirect, url_for
from models import Pack, Charm

emoticharms = Blueprint("emoticharms", __name__, url_prefix="/emoticharms")


@emoticharms.route('/')
def index():
    packs = Pack.query.all()
    charms = Charm.query.all()
    raise NotImplementedError()

@emoticharms.route('/manage')
def manage():
    raise NotImplementedError()