from flask import Blueprint, flash, redirect, url_for
from models import Pack

emoticharms = Blueprint("emoticharms", __name__, url_prefix="/emoticharms")


@emoticharms.route('/')
def index():
    packs = Pack.query.all()
    raise NotImplementedError()

@emoticharms.route('/manage')
def manage():
    raise NotImplementedError()