from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from hfsa_app.extensions import db,bcrypt
from hfsa_app.extensions import migrate
from flask_jwt_extended import JWTManager
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import Flask, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask import send_from_directory
import os  
from flask_cors import CORS

#importing bluebrints
from hfsa_app.controllers.user_controller import user_bp
from hfsa_app.controllers.program_controller import program_bp
from hfsa_app.controllers.events_controller import event_bp
from hfsa_app.controllers.gallery_controllers import gallery_bp
from hfsa_app.controllers.contact_inquiry_controller import contact_inquiry_bp
from hfsa_app.controllers.donations_controller import donation_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    # Initialize database
    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)

    # Initialize JWTManager with secret key
    app.config['JWT_SECRET_KEY'] = '12345'  
    jwt = JWTManager(app)


    #importing models
    from hfsa_app.models import user
    from hfsa_app.models import gallery
    from hfsa_app.models import program
    from hfsa_app.models import events
    from hfsa_app.models import contact_inquiry
    from hfsa_app.models import donations
    

     # Import blueprints
    from hfsa_app.controllers.user_controller import User
    

    # Register blueprints
    app.register_blueprint(user_bp,url_prefix='/api/v1/user')
    app.register_blueprint(program_bp,url_prefix='/api/v1/program')
    app.register_blueprint(event_bp,url_prefix='/api/v1/event')
    app.register_blueprint(gallery_bp,url_prefix='/api/v1/gallery')
    app.register_blueprint(contact_inquiry_bp,url_prefix='/api/v1/contact-inquiry')
    app.register_blueprint(donation_bp,url_prefix='/api/v1/donation')
    


    # Serve Swagger JSON file
    @app.route('/swagger.json')
    def serve_swagger_json():
        try:
            return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

        except FileNotFoundError:
            return jsonify({"message": "Swagger JSON file not found"}), 404
        
    # Swagger UI configuration
    SWAGGER_URL = '/api/docs'  
    API_URL = '/swagger.json'  
    
    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  
            'app_name': "hope_field_sports_academy_app"
        }
    )
    
    # Register Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint)


    @app.route('/')
    def home():
        return 'Welcome to Hope Field Sports Academy!'
    
    # Routes for protected resources
    @app.route('/protected')
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
