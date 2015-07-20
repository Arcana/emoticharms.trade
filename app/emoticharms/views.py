from flask import Blueprint, flash, redirect, url_for, render_template
from models import Pack
from forms import UserPacksForm
from ..util import valid_ti5_ticket
from flask.ext.login import login_required

emoticharms = Blueprint("emoticharms", __name__, url_prefix="/emoticharms")


@emoticharms.route('/')
@login_required
@valid_ti5_ticket
def index():
    packs = Pack.query.all()
    return render_template('emoticharms/index.html', packs=packs)


@emoticharms.route('/manage')
@login_required
@valid_ti5_ticket
def manage():
    form = UserPacksForm()
    return render_template('emoticharms/manage.html', form=form)
