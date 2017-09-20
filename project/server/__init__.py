# project/server/__init__.py


#################
#### imports ####
#################

import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


################
#### config ####
################

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)

app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)


####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


###################
### blueprints ####
###################

from project.server.user.views import user_blueprint
from project.server.main.views import main_blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(main_blueprint)


#####################
#### flask-login ####
#####################

from project.server.models import User

login_manager.login_view = "user.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

#####################
#### flask-admin ####
#####################

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

from project.server.models import Appointment
from project.server.models import Treatment
from project.server.models import Symptom
from project.server.models import User_Symptom
from project.server.models import User_Symptom_Treatment
from project.server.models import Attachment
from project.server.models import Provider

admin = Admin(app)

class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Appointment, db.session))
admin.add_view(ModelView(Treatment, db.session))
admin.add_view(ModelView(Symptom, db.session))
admin.add_view(ModelView(User_Symptom, db.session))
admin.add_view(ModelView(User_Symptom_Treatment, db.session))
admin.add_view(ModelView(Attachment, db.session))
admin.add_view(ModelView(Provider, db.session))

########################
#### error handlers ####
########################

@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
