from flask import flash, abort
from flask.ext.login import current_user
from functools import wraps


#Decorators
def valid_ti5_ticket(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.ti5_ticket:
            flash('Valid International 2015 ticket required.', 'danger')
            return abort(403)
        return func(*args, **kwargs)
    return decorated_function