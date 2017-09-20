# project/server/models.py
# https://gist.github.com/kirang89/10030736

import datetime
from sqlalchemy.ext.declarative import declared_attr

from project.server import app, db, bcrypt

Base = db.Model

class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Attachments
    @declared_attr
    def attachment(cls):
        field = cls.__name__.lower()
        return db.relationship('Attachment', backref=field, lazy='dynamic')


class User(BaseModel, Base):

    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zip_code = db.Column(db.Integer, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    symptoms = db.relationship('Symptom', secondary='user_symptom')
    appointments = db.relationship('Appointment', backref='users', lazy='dynamic')

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Appointment(BaseModel, Base):
    """"""
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    treatments = db.relationship('Treatment', secondary='user_symptom_treatment')


class Treatment(BaseModel, Base):
    """"""
    name = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, nullable=False)


class Symptom(BaseModel, Base):
    """"""
    name = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, nullable=False)


class User_Symptom(BaseModel, Base):
    """"""
    __tablename__ = 'user_symptom'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    treatments = db.relationship('Treatment', secondary='user_symptom_treatment')


class User_Symptom_Treatment(BaseModel, Base):
    """"""
    __tablename__ = 'user_symptom_treatment'
    user_symptom_id = db.Column(db.Integer, db.ForeignKey('user_symptom.id'))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)


class Attachment(Base):
    """"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(4096), nullable=False)
    attachment_type = db.Column(db.String(255), nullable=True)

    # Tables for attachments
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'))
    user_symptom_id = db.Column(db.Integer, db.ForeignKey('user_symptom.id'))
    user_symptom_treatment_id = db.Column(db.Integer, db.ForeignKey('user_symptom_treatment.id'))
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))


class Provider(BaseModel, Base):
	""""""
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80), nullable=False)
	suffix = db.Column(db.String(8), nullable=True)
	specialty = db.Column(db.String(80), nullable=True)
