from flask import Blueprint, render_template
from models import Pack
from forms import UserPacksForm
from ..util import valid_ti5_ticket
from flask.ext.login import login_required

emoticharms = Blueprint("emoticharms", __name__)


@emoticharms.route('/stickerbook', methods=['GET', 'POST'])
@login_required
@valid_ti5_ticket
def stickerbook():
    return render_template('emoticharms/stickerbook.html', form=UserPacksForm())
