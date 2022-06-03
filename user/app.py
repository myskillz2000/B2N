from statistics import mode
from flask import Flask
from flask_migrate import Migrate
import models
from routes import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Matt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/user.db'
models.init_app(app)

app.register_blueprint(user_blueprint)

migrate = Migrate(app,models.db)

if __name__=='__main__':
    app.run(debug=True)