from flask import Blueprint, request, jsonify
from hfsa_app import db
from hfsa_app.models.gallery import Gallery

gallery_bp = Blueprint('gallery', __name__, url_prefix='/api/v1/gallery')

# Get all images in the gallery (public access)
@gallery_bp.route('/images', methods=['GET'])
def get_all_images():
    images = Gallery.query.all()
    output = []
    for image in images:
        image_data = {
            'id': image.id,
            'title': image.title,
            'description': image.description,
            'image_url': image.image_url,
            'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        output.append(image_data)
    return jsonify({'images': output})

# Get a specific image by ID (public access)
@gallery_bp.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    image = Gallery.query.get_or_404(id)
    image_data = {
        'id': image.id,
        'title': image.title,
        'description': image.description,
        'image_url': image.image_url,
        'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(image_data)

# Upload a new image to the gallery (public access)
@gallery_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        new_image = Gallery(
            title=data.get('title'),
            description=data.get('description'),
            image_url=data.get('image_url')
        )
        db.session.add(new_image)
        db.session.commit()
        image_data = {
            'id': new_image.id,
            'title': new_image.title,
            'description': new_image.description,
            'image_url': new_image.image_url,
            'upload_date': new_image.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'message': 'Image uploaded successfully', 'image': image_data}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an image in the gallery (public access)
@gallery_bp.route('/image/<int:id>', methods=['PUT'])
def update_image(id):
    image = Gallery.query.get_or_404(id)
    data = request.get_json()
    try:
        image.title = data.get('title', image.title)
        image.description = data.get('description', image.description)
        image.image_url = data.get('image_url', image.image_url)
        db.session.commit()
        image_data = {
            'id': image.id,
            'title': image.title,
            'description': image.description,
            'image_url': image.image_url,
            'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'message': 'Image updated successfully', 'image': image_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete an image from the gallery (public access)
@gallery_bp.route('/image/<int:id>', methods=['DELETE'])
def delete_image(id):
    image = Gallery.query.get_or_404(id)
    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': 'Image deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete image', 'details': str(e)}), 500
