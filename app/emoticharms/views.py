from app import db
from app.emoticharms.models import UserPack
from flask import Blueprint, render_template, request
from forms import UserPacksForm, PackQuantityField
from ..util import valid_ti5_ticket
from flask.ext.login import login_required, current_user

emoticharms = Blueprint("emoticharms", __name__)


@emoticharms.route('/stickerbook', methods=['GET', 'POST'])
@login_required
@valid_ti5_ticket
def stickerbook():
    if request.method == 'GET':
        form_data = {
            user_pack.pack.normalized_name: user_pack.quantity
            for user_pack in UserPack.query.filter_by(user=current_user).all()
        }
        form = UserPacksForm(data=form_data)
    elif request.method == 'POST':
        form = UserPacksForm(request.form)
        if form.validate():
            for field in form:
                if not isinstance(field, PackQuantityField):
                    continue
                user_pack = UserPack.query.filter_by(pack_id=field.pack.id, user_id=current_user.account_id).first()
                if user_pack is None:
                    user_pack = UserPack(field.pack.id, current_user.account_id, field.data)
                    db.session.add(user_pack)
                else:
                    user_pack.quantity = field.data
                db.session.commit()

    return render_template('emoticharms/stickerbook.html', form=form)
