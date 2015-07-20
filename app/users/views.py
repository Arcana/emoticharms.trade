from flask import Blueprint, flash, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import oid, db, login_manager
from models import User, AnonymousUser
from sqlalchemy.exc import IntegrityError
import datetime


users = Blueprint("users", __name__, url_prefix="/users")

login_manager.anonymous_user = AnonymousUser


# User authentication
@login_manager.user_loader
def load_user(user_id):
    _user = User.query.get(user_id)
    if _user:
        _user.update_last_seen()
    if _user and _user.enabled is False:
        logout_user()
        flash("You have been banned from using this website.", "danger")
        redirect(url_for("index"))
    return _user


@users.route('/login/')
@oid.loginhandler
def login():
    if current_user.is_authenticated():
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')


@oid.after_login
def create_or_login(resp):
    steam_id = long(resp.identity_url.replace("http://steamcommunity.com/openid/id/", ""))
    account_id = int(steam_id & 0xFFFFFFFF)
    _user = User.query.get(account_id)
    new_user = False

    if not _user:
        _user = User(account_id)
        new_user = True
        db.session.add(_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            _user = User.query.get(account_id)

    if not _user.signed_in:
        _user.signed_in = True
        db.session.add(_user)
        db.session.commit()

    if not _user.is_active():
        flash(u"Cannot log you in, {}. You are banned.".format(_user.name), "danger")
        return redirect(oid.get_next_url())

    login_attempt = login_user(_user, remember=True)
    if login_attempt is True and new_user and _user.ti5_ticket is True and _user.profile_url:
        flash(u"Welcome to emoticharms.trade, {}!".format(_user.name), "success")
    elif login_attempt is True and new_user and _user.ti5_ticket is False and _user.profile_url:
        flash(u"Welcome to emoticharms.trade, {}! Unfortunately you do not appear to have an International 2015 ticket "
              u"associated with your Steam account. This site is only available to users with TI5 tickets. "
              u"If you have a ticket, please associate it with your Steam account "
              u"and then recheck status from your settings page.".format(_user.name), "warning")
    elif login_attempt is True and new_user and not _user.profile_url:
        flash(u"Welcome to emoticharms.trade! Unfortunately were unable to fetch your Steam user data."
              u"We will try again soon. For now you will be represented by your numerical ID, {}.".format(_user.name)
              , "success")
    elif login_attempt is True and not new_user:
        flash(u"Welcome back, {}.".format(_user.name), "success")
    else:
        flash(u"Error logging you in as {}, please try again later.".format(_user.name), "danger")
    return redirect(oid.get_next_url())


@users.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u"You are now logged out.")
    return redirect(oid.get_next_url())


@users.route('/settings/')
@login_required
def settings():
    show_button = False
    if not current_user.ti5_ticket:
        show_button = datetime.datetime.utcnow() + datetime.timedelta(hours=2) > current_user.next_steam_check
    return render_template('users/settings.html', show_button=show_button)


@users.route('/check_ticket/')
@login_required
def check_ticket():
    if not current_user.ti5_ticket:
        if datetime.datetime.utcnow() + datetime.timedelta(hours=2) > current_user.next_steam_check:
            current_user.fetch_steam_info()
            db.session.add(current_user)
            db.session.commit()
            if current_user.ti5_ticket:
                flash('Success. Your ticket has been successfully validated. You now have full access to the site.', 'success')
            else:
                flash('Your ticket has not been validated. Please ensure that it is correctly linked.', 'danger')
        else:
            flash('Please wait a few more hours before rechecking.', 'danger')
    else:
        flash('Your account already has an International 2015 ticket associated.', 'success')
    return redirect(url_for('users.settings'))