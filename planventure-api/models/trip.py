from datetime import datetime, timedelta

from database import BaseModel, db


class Trip(BaseModel):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False) # Added name column
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    itinerary = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.String(255))  # Add this line
    
    # Relationship
    user = db.relationship('User', back_populates='trips')

    @staticmethod
    def generate_default_itinerary(start_date, end_date):
        """
        Generate a default itinerary template for the trip duration
        Returns a JSON structure with daily activities
        """
        itinerary = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            itinerary[date_str] = {
                "morning": {
                    "time": "09:00",
                    "activity": "Breakfast and Planning",
                    "location": "",
                    "notes": ""
                },
                "afternoon": {
                    "time": "13:00",
                    "activity": "Sightseeing",
                    "location": "",
                    "notes": ""
                },
                "evening": {
                    "time": "19:00",
                    "activity": "Dinner",
                    "location": "",
                    "notes": ""
                }
            }
            current_date += timedelta(days=1)
        
        return itinerary

    def __repr__(self):
        return f'<Trip {self.destination} ({self.start_date} - {self.end_date})>'
