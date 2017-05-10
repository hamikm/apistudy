from app import db

class Listing(db.Model):
    '''Table of listings for SpaceBnB'''
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    title = db.Column(db.String(140))
    description = db.Column(db.String(1024))
    expiration = db.Column(db.DateTime)
    locationX = db.Column(db.Float)
    locationY = db.Column(db.Float)

    def __repr__(self):
        return ('Listing: {} posted {} at ({}, {}). It expires {}'.format(
            self.user, self.title, self.locationX, self.locationY, self.expiration))

    
