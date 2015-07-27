from flask.ext.wtf import Form
from wtforms import StringField, SubmitField


class UserSettings(Form):
    email = StringField('Email:')
    submit = SubmitField('Save')