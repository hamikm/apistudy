from datetime import datetime

from app import app, models, db
from flask import request

@app.route('/health')
def health():
    return 'ok'

@app.route('/api/listings', methods=['POST'])
def postListing():
    content = request.get_json(silent=True)
    
    if models.Listing.validate(content):
        listing = models.Listing(
            user=content.get('user'),
            title=content.get('title'),
            description=content.get('description'),
            expiration=models.Listing.parseDate(content.get('expiration')),
            locationX=content.get('location').get('x'),
            locationY=content.get('location').get('y')
        )

        try:
            db.session.add(listing)
            db.session.commit()
        except Exception as e:
            print '============> ', e 
            return 'nay' # TODO return 404

        return 'yayyyy'
    else:
        return 'nay'

