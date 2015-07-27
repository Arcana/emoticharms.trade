from app import db
from app.emoticharms.models import UserPack
from flask import Blueprint, render_template, request, url_for, redirect
from app.users.models import User
from forms import UserPacksForm, PackQuantityField
from ..util import valid_ti5_ticket
from flask.ext.login import login_required, current_user

emoticharms = Blueprint("emoticharms", __name__)


@emoticharms.route('/collection/', methods=['GET', 'POST'])
@login_required
@valid_ti5_ticket
def collection():

    form = UserPacksForm()

    if form.validate_on_submit():
        print 'submitted'
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

    form_data = {
        user_pack.pack.normalized_name: user_pack.quantity
        for user_pack in UserPack.query.filter_by(user=current_user).all()
        }
    print form_data
    form = UserPacksForm(data=form_data)

    return render_template('emoticharms/collection.html', form=form)

@emoticharms.route('/collection/matches/')
@login_required
@valid_ti5_ticket
def matches():
    """
    Match with other users by the count of packs the other party has that we want,
    and that the other party wants and we have. Ordered by the most amount of combined packs matched.
    """

    # Get ids of own packs where we own 0 (we need)
    wanted_packs = UserPack.query.filter(UserPack.user_id == current_user.account_id, UserPack.quantity == 0).all()
    spare_packs  = UserPack.query.filter(UserPack.user_id == current_user.account_id, UserPack.quantity > 1).all()

    wanted_pack_ids = [unicode(user_pack.pack_id) for user_pack in wanted_packs]
    spare_pack_ids  = [unicode(user_pack.pack_id) for user_pack in spare_packs]

    # Get ids of owned packs that are greater than 1 (our dupes)
    matches_query = db.engine.execute("""
    SELECT
        account_id,
        SUM(spare_count) as other_user_has_spare_count,
        SUM(want_count) as other_user_wants_count,
        (spare_count + want_count) as total_count
    FROM (
        SELECT u.account_id, COUNT(*) as spare_count, 0 as want_count
        FROM users u
        INNER JOIN user_pack up
        ON up.user_id = u.account_id AND up.pack_id IN ({wanted_pack_ids}) AND up.quantity > 1
        GROUP BY u.account_id

        UNION

        SELECT u.account_id, 0 as spare_count, COUNT(*) as want_count
        FROM users u
        INNER JOIN user_pack up
        ON up.user_id = u.account_id AND up.pack_id IN ({spare_pack_ids}) AND up.quantity = 0
        GROUP BY u.account_id
    ) counts_table

    GROUP BY counts_table.account_id

    ORDER BY total_count desc
    """.format(
            wanted_pack_ids=','.join(wanted_pack_ids),
            spare_pack_ids=','.join(spare_pack_ids)
        )
    )

    # Attach user objects (probably a lot better way to do this)
    matches = []
    for match in matches_query:
        matches.append({
            'user': User.query.filter(User.account_id == match[0]).first(),
            'other_user_has_spare_count': match[1],
            'other_user_wants_count': match[2]
        })

    return render_template('emoticharms/matches.html',
                           wanted_packs=wanted_packs,
                           spare_packs=spare_packs,
                           matches=matches)