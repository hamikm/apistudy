from app import db
import json
from datetime import datetime

class Listing(db.Model):
    '''Define table of listings for SpaceBnB'''
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    title = db.Column(db.String(140))
    description = db.Column(db.String(1024))
    expiration = db.Column(db.DateTime)
    locationX = db.Column(db.Float)
    locationY = db.Column(db.Float)

    DATEFORMAT = "%Y-%m-%dT%H:%M:%S"
    
    def __repr__(self):
        return ('Listing: {} posted {} at ({}, {}). It expires {}'.format(
            self.user, self.title, self.locationX, self.locationY, self.expiration))

    def toDict(self):
        '''Return self as a jsonifiable dictionary'''
        return {
            'id': self.id,
            'user': self.user,
            'title': self.title,
            'description': self.description,
            'expiration': str(self.expiration),
            'location': {
                'x': self.locationX,
                'y': self.locationY
            }
        }
    
    @classmethod
    def parseDate(cls, dateStr):
        '''Convert string date to datetime object'''
        try:
            return dateStr and datetime.strptime(dateStr, cls.DATEFORMAT)
        except:
            return None
            
    @classmethod
    def validate(cls, listingJson):
        '''Validates json listings'''
        user = listingJson.get('user')
        title = listingJson.get('title')
        description = listingJson.get('description')
        expirationStr = listingJson.get('expiration')
        locationX = listingJson.get('location') and listingJson.get('location').get('x')
        locationY = listingJson.get('location') and listingJson.get('location').get('y')
        expiration = cls.parseDate(expirationStr)
        
        return (user and type(user) == unicode
            and title and type(title) == unicode
            and description and type(description) == unicode
            and expiration and type(expiration) == datetime
            and locationX and type(locationX) == float
            and locationY and type(locationY) == float
        )


