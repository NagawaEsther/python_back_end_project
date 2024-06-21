from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from hfsa_app.models.donations import Donation
from hfsa_app import db
from datetime import datetime
from functools import wraps

donation_bp = Blueprint('donation', __name__, url_prefix='/api/v1/donation')


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

# Create a new donation
@donation_bp.route('/create', methods=['POST'])
def create_donation():
    try:
        data = request.get_json()
        donor_name = data.get('donor_name')
        donor_email = data.get('donor_email')
        donation_amount = data.get('donation_amount')
        message = data.get('message')

        if not donor_name or not donor_email or not donation_amount:
            return jsonify({'error': 'Missing required fields (donor_name, donor_email, donation_amount)'}), 400

        new_donation = Donation(
            donor_name=donor_name,
            donor_email=donor_email,
            donation_amount=donation_amount,
            message=message
        )

        db.session.add(new_donation)
        db.session.commit()

        donation_data = {
            'id': new_donation.id,
            'donor_name': new_donation.donor_name,
            'donor_email': new_donation.donor_email,
            'donation_amount': new_donation.donation_amount,
            'donation_date': new_donation.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': new_donation.message,
        }

        return jsonify({'message': 'Donated successfully', 'donation': donation_data}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all donations
@donation_bp.route('/donations', methods=['GET'])
@admin_required
def get_all_donations():
    try:
        donations = Donation.query.all()
        output = []
        for donation in donations:
            donation_data = {
                'id': donation.id,
                'donor_name': donation.donor_name,
                'donor_email': donation.donor_email,
                'donation_amount': donation.donation_amount,
                'donation_date': donation.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
                'message': donation.message,
            }
            output.append(donation_data)
        return jsonify({'donations': output})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific donation
@donation_bp.route('/donation/<int:id>', methods=['GET'])
@admin_required
def get_donation(id):
    try:
        donation = Donation.query.get_or_404(id)
        donation_data = {
            'id': donation.id,
            'donor_name': donation.donor_name,
            'donor_email': donation.donor_email,
            'donation_amount': donation.donation_amount,
            'donation_date': donation.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': donation.message,
        }
        return jsonify(donation_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a donation (public access with email verification)
@donation_bp.route('/donation/<int:id>', methods=['PUT'])
@jwt_required()
def update_donation(id):
    donation = Donation.query.get_or_404(id)
    data = request.get_json()
    user_info = get_jwt_identity()

    if data.get('donor_email') != donation.donor_email:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        donation.donor_name = data.get('donor_name', donation.donor_name)
        donation.donor_email = data.get('donor_email', donation.donor_email)
        donation.donation_amount = data.get('donation_amount', donation.donation_amount)
        donation.message = data.get('message', donation.message)

        db.session.commit()

        donation_data = {
            'id': donation.id,
            'donor_name': donation.donor_name,
            'donor_email': donation.donor_email,
            'donation_amount': donation.donation_amount,
            'donation_date': donation.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': donation.message,
        }

        return jsonify({'message': 'Donation updated successfully', 'donation': donation_data})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a donation (public access with email verification)
@donation_bp.route('/donation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_donation(id):
    donation = Donation.query.get_or_404(id)
    data = request.get_json()
    user_info = get_jwt_identity()

    if data.get('donor_email') != donation.donor_email:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        db.session.delete(donation)
        db.session.commit()
        return jsonify({'message': 'Donation deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete donation', 'details': str(e)}), 500