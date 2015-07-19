from flask import Blueprint, flash, redirect, url_for, render_template
from app.emoticharms.models import Pack, Charm
from app.emoticharms.forms import UserPacksForm

emoticharms = Blueprint("emoticharms", __name__, url_prefix="/emoticharms")


@emoticharms.route('/')
def index():
    packs = Pack.query.all()
    return render_template('emoticharms/index.html', packs=packs)


@emoticharms.route('/manage')
def manage():
    form = UserPacksForm()
    return render_template('emoticharms/manage.html', form=form)
