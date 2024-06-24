from flask import Blueprint, request, jsonify
from hfsa_app import db
from hfsa_app.models.contact_inquiry import ContactInquiry
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

contact_inquiry_bp = Blueprint('contact_inquiry', __name__, url_prefix='/api/v1/contact-inquiry')


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

# Create a new contact inquiry (public access)
@contact_inquiry_bp.route('/create', methods=['POST'])
def create_contact_inquiry():
    try:
        data = request.get_json()
        new_inquiry = ContactInquiry(
            name=data.get('name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        db.session.add(new_inquiry)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully', 'inquiry': {
            'id': new_inquiry.id,
            'name': new_inquiry.name,
            'email': new_inquiry.email,
            'subject': new_inquiry.subject,
            'message': new_inquiry.message,
            'received_date': new_inquiry.received_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': new_inquiry.status
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all contact inquiries 
@contact_inquiry_bp.route('/inquiries', methods=['GET'])
@admin_required
def get_all_contact_inquiries():
    inquiries = ContactInquiry.query.all()
    output = []
    for inquiry in inquiries:
        inquiry_data = {
            'id': inquiry.id,
            'name': inquiry.name,
            'email': inquiry.email,
            'subject': inquiry.subject,
            'message': inquiry.message,
            'received_date': inquiry.received_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': inquiry.status
        }
        output.append(inquiry_data)
    return jsonify({'inquiries': output})

# Get a specific contact inquiry 
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['GET'])
@admin_required
def get_contact_inquiry(id):
    inquiry = ContactInquiry.query.get_or_404(id)
    inquiry_data = {
        'id': inquiry.id,
        'name': inquiry.name,
        'email': inquiry.email,
        'subject': inquiry.subject,
        'message': inquiry.message,
        'received_date': inquiry.received_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': inquiry.status
    }
    return jsonify(inquiry_data)

# Update a contact inquiry 
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['PUT'])
@admin_required  
def update_contact_inquiry(id):
    inquiry = ContactInquiry.query.get_or_404(id)
    data = request.get_json()

    if data.get('email') != inquiry.email:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        inquiry.name = data.get('name', inquiry.name)
        inquiry.subject = data.get('subject', inquiry.subject)
        inquiry.message = data.get('message', inquiry.message)
        
        db.session.commit()
        return jsonify({'message': 'Contact inquiry updated successfully', 'inquiry': {
            'id': inquiry.id,
            'name': inquiry.name,
            'email': inquiry.email,
            'subject': inquiry.subject,
            'message': inquiry.message,
            'received_date': inquiry.received_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': inquiry.status
        }})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a contact inquiry 
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['DELETE'])
@admin_required  
def delete_contact_inquiry(id):
    try:
        inquiry = ContactInquiry.query.get_or_404(id)
        db.session.delete(inquiry)
        db.session.commit()
        return jsonify({'message': 'Contact inquiry deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete contact inquiry', 'details': str(e)}), 500
