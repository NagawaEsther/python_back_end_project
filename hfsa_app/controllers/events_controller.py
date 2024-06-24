from flask import Blueprint, request, jsonify
from hfsa_app import db
from hfsa_app.models.events import Event
from datetime import datetime
from flask_jwt_extended import jwt_required,get_jwt_identity
from functools import wraps

event_bp = Blueprint('event', __name__, url_prefix='/api/v1/event')

# Admin required decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Get all events
@event_bp.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    output = []
    for event in events:
        event_data = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M'),
            'location': event.location,
            'registration_required': event.registration_required,
            'max_participants': event.max_participants
        }
        output.append(event_data)
    return jsonify({'events': output})

# Get a specific event
@event_bp.route('/event/<int:id>', methods=['GET'])
@admin_required
def get_event(id):
    event = Event.query.get_or_404(id)
    event_data = {
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d'),
        'time': event.time.strftime('%H:%M'),
        'location': event.location,
        'registration_required': event.registration_required,
        'max_participants': event.max_participants
    }
    return jsonify(event_data)

# Create a new event
@event_bp.route('/create', methods=['POST'])
@admin_required
def create_event():
    try:
        data = request.get_json()
        new_event = Event(
            name=data['name'],
            description=data['description'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            time=datetime.strptime(data['time'], '%H:%M'),
            location=data['location'],
            registration_required=data['registration_required'],
            max_participants=data.get('max_participants')
        )
        db.session.add(new_event)
        db.session.commit()

        event_data = {
            'id': new_event.id,
            'name': new_event.name,
            'description': new_event.description,
            'date': new_event.date.strftime('%Y-%m-%d'),
            'time': new_event.time.strftime('%H:%M'),
            'location': new_event.location,
            'registration_required': new_event.registration_required,
            'max_participants': new_event.max_participants
        }

        return jsonify({
            'message': 'Event created successfully',
            'event': event_data
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an event
@event_bp.route('/event/<int:id>', methods=['PUT'])
@admin_required
def update_event(id):
    try:
        event = Event.query.get_or_404(id)
        data = request.get_json()

        event.name = data.get('name', event.name)
        event.description = data.get('description', event.description)
        event.date = datetime.strptime(data['date'], '%Y-%m-%d')
        event.time = datetime.strptime(data['time'], '%H:%M')  
        event.location = data.get('location', event.location)
        event.registration_required = data.get('registration_required', event.registration_required)
        event.max_participants = data.get('max_participants', event.max_participants)
        
        db.session.commit()

        event_data = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M'),
            'location': event.location,
            'registration_required': event.registration_required,
            'max_participants': event.max_participants
        }

        return jsonify({
            'message': 'Event updated successfully',
            'event': event_data
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an event
@event_bp.route('/event/<int:id>', methods=['DELETE'])
@admin_required
def delete_event(id):
    try:
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete event', 'details': str(e)}), 500
