from flask import Blueprint, request, jsonify
from hfsa_app import db
from hfsa_app.models.contact_inquiry import ContactInquiry

contact_inquiry_bp = Blueprint('contact_inquiry', __name__, url_prefix='/api/v1/contact-inquiry')

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

# Get all contact inquiries (public access)
@contact_inquiry_bp.route('/inquiries', methods=['GET'])
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

# Get a specific contact inquiry (public access)
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['GET'])
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

# Update a contact inquiry (public access with email verification)
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['PUT'])
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

# Delete a contact inquiry (public access with email verification)
@contact_inquiry_bp.route('/inquiry/<int:id>', methods=['DELETE'])
def delete_contact_inquiry(id):
    inquiry = ContactInquiry.query.get_or_404(id)
    data = request.get_json()

    if data.get('email') != inquiry.email:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        db.session.delete(inquiry)
        db.session.commit()
        return jsonify({'message': 'Contact inquiry deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete contact inquiry', 'details': str(e)}), 500
