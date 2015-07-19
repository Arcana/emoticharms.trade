from flask import Blueprint, flash, redirect, url_for, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import oid, db, login_manager
from models import User, AnonymousUser
from sqlalchemy.exc import IntegrityError


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
    return render_template('users/settings.html')