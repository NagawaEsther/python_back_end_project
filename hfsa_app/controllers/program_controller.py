from flask import Blueprint, request, jsonify
from hfsa_app import db
from hfsa_app.models.program import Program
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from functools import wraps

program_bp = Blueprint('program', __name__, url_prefix='/api/v1/program')

#Admin required
def admin_required(fn):
    @wraps(fn)
    @jwt_required()  
    def wrapper(*args, **kwargs):
        user_info = get_jwt_identity()
        if user_info['role'] != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# Get all programs
@program_bp.route('/programs', methods=['GET'])
def get_all_programs():
    programs = Program.query.all()
    output = []
    for program in programs:
        program_data = {
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'schedule': program.schedule,
            'capacity': program.capacity,
            'duration': program.duration,
            'fees': program.fees,
            'created_at': program.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': program.updated_at.strftime('%Y-%m-%d %H:%M:%S') if program.updated_at else None
        }
        output.append(program_data)
    return jsonify({'programs': output})

# Get a specific program
@program_bp.route('/program/<int:id>', methods=['GET'])
@admin_required
def get_program(id):
    program = Program.query.get_or_404(id)
    program_data = {
        'id': program.id,
        'name': program.name,
        'description': program.description,
        'schedule': program.schedule,
        'capacity': program.capacity,
        'duration': program.duration,
        'fees': program.fees,
        'created_at': program.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': program.updated_at.strftime('%Y-%m-%d %H:%M:%S') if program.updated_at else None
    }
    return jsonify(program_data)

# Create a new program
@program_bp.route('/register', methods=['POST'])
@admin_required
def create_program():
    try:
        data = request.get_json()
        new_program = Program(
            name=data['name'],
            description=data['description'],
            schedule=data['schedule'],
            capacity=data['capacity'],
            duration=data['duration'],
            fees=data['fees']
        )
        db.session.add(new_program)
        db.session.commit()

        program_data = {
            'id': new_program.id,
            'name': new_program.name,
            'description': new_program.description,
            'schedule': new_program.schedule,
            'capacity': new_program.capacity,
            'duration': new_program.duration,
            'fees': new_program.fees,
            'created_at': new_program.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': new_program.updated_at.strftime('%Y-%m-%d %H:%M:%S') if new_program.updated_at else None
        }

        return jsonify({
            'message': 'Program created successfully',
            'program': program_data
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update a program
@program_bp.route('/program/<int:id>', methods=['PUT'])
@admin_required
def update_program(id):
    try:
        program = Program.query.get_or_404(id)
        data = request.get_json()

        program.name = data.get('name', program.name)
        program.description = data.get('description', program.description)
        program.schedule = data.get('schedule', program.schedule)
        program.capacity = data.get('capacity', program.capacity)
        program.duration = data.get('duration', program.duration)
        program.fees = data.get('fees', program.fees)
        program.updated_at = datetime.now()
        
        db.session.commit()

        program_data = {
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'schedule': program.schedule,
            'capacity': program.capacity,
            'duration': program.duration,
            'fees': program.fees,
            'created_at': program.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': program.updated_at.strftime('%Y-%m-%d %H:%M:%S') if program.updated_at else None
        }

        return jsonify({
            'message': 'Program updated successfully',
            'program': program_data
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a program
@program_bp.route('/program/<int:id>', methods=['DELETE'])
@admin_required
def delete_program(id):
    try:
        program = Program.query.get_or_404(id)
        db.session.delete(program)
        db.session.commit()
        return jsonify({'message': 'Program deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete program', 'details': str(e)}), 500
