from flask import flash, abort, render_template
from flask.ext.login import current_user
from functools import wraps


#Decorators
def valid_ti5_ticket(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.ti5_ticket:
            return render_template('errors/ticket_required.html'), 403
        return func(*args, **kwargs)
    return decorated_function