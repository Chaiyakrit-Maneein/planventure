from datetime import datetime

from database import db
from flask import Blueprint, g, jsonify, request
from models.trip import Trip
from routes.auth import auth_required
from utils.error_handlers import create_error_response

trip_bp = Blueprint('trip', __name__)

class TripFactory:
    @staticmethod
    def create_trip(data: dict, user_id: int) -> Trip:
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        except (KeyError, ValueError):
            raise ValueError("Invalid or missing date format. Use YYYY-MM-DD")
            
        if not data.get('name') or not data.get('destination'):
            raise ValueError("Missing required fields: name and destination")
            
        return Trip(
            name=data['name'],
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            description=data.get('description', ''),
            itinerary=Trip.generate_default_itinerary(start_date, end_date),
            user_id=user_id
        )

@trip_bp.route('/trips', methods=['POST'])
@auth_required
def create_trip():
    data = request.get_json()
    try:
        trip = TripFactory.create_trip(data, g.current_user.id)
    except ValueError as e:
        return jsonify(create_error_response("TRIP_001", str(e), 400)), 400

    db.session.add(trip)
    db.session.commit()
    return jsonify({
        'message': 'Trip created',
        'trip': {
            'id': trip.id,
            'name': trip.name,
            'destination': trip.destination,
            'start_date': trip.start_date.strftime('%Y-%m-%d'),
            'end_date': trip.end_date.strftime('%Y-%m-%d'),
            'description': trip.description,
            'itinerary': trip.itinerary
        }
    }), 201

@trip_bp.route('/trips', methods=['GET'])
@auth_required
def get_trips():
    trips = Trip.query.filter_by(user_id=g.current_user.id).all()
    trips_data = [{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'destination': t.destination,
        'start_date': t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
        'end_date': t.end_date.strftime('%Y-%m-%d') if t.end_date else None
    } for t in trips]
    return jsonify({'trips': trips_data}), 200

@trip_bp.route('/trips/<int:trip_id>', methods=['GET'])
@auth_required
def get_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=g.current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    return jsonify({'trip': {
        'id': trip.id,
        'name': trip.name,
        'description': trip.description,
        'destination': trip.destination,
        'start_date': trip.start_date.strftime('%Y-%m-%d') if trip.start_date else None,
        'end_date': trip.end_date.strftime('%Y-%m-%d') if trip.end_date else None
    }}), 200

@trip_bp.route('/trips/<int:trip_id>', methods=['PUT'])
@auth_required
def update_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=g.current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    data = request.get_json()
    if data.get('name'):
        trip.name = data['name']
    if data.get('description') is not None:
        trip.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Trip updated', 'trip': {'id': trip.id, 'name': trip.name, 'description': trip.description}}), 200

@trip_bp.route('/trips/<int:trip_id>', methods=['DELETE'])
@auth_required
def delete_trip(trip_id):
    trip = Trip.query.filter_by(id=trip_id, user_id=g.current_user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': 'Trip deleted'}), 200
