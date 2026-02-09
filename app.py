from flask import Flask
from config import Config
from extensions import mongo, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register routes
    from routes.auth_routes import auth_bp
    from routes.vote_routes import vote_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vote_bp, url_prefix="/api/vote")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
