from datetime import datetime

from app import app, models, db
from flask import request, jsonify, abort, make_response

def makeError(statusCode, msg):
    ret = jsonify({
        'status': statusCode,
        'message': msg
    })
    ret.status_code = statusCode
    return ret

@app.route('/health')
def health():
    return 'ok'

@app.route('/api/listings', methods=['GET'])
def getListings():
    '''Get and return listings using the given query args'''

    active = True if request.args.get('active') == '1' else False
    lengthStr = request.args.get('length')
    pageStr = request.args.get('page')
    length, page = -1, -1

    # Convert length and page args into ints if they exist, then return
    # paginated listings
    if lengthStr and pageStr:
        length = int(lengthStr)
        page = int(pageStr)
        listings = []
        if length < 1 or page < 1:
            return makeError(400, "page and length must be nonnegative")
        for idNum in range(length * (page - 1) + 1, length * page + 1):
            currListing = models.Listing.query.get(idNum)
            if (not currListing) or (active and datetime.now() > currListing.expiration):
                continue # skip expired listings if we only want active ones
            listings.append(currListing.toDict())
        return jsonify(listings)

    # Otherwise just return all listings
    else:
        listings = []
        allListings = models.Listing.query.all()
        for listing in allListings:
            if active and datetime.now() > listing.expiration:
                continue # skip expired listings if we only want active ones
            listings.append(listing.toDict())
        return jsonify(listings)

@app.route('/api/listings', methods=['POST'])
def postListing():
    '''Insert the listing, which is passed via JSON, as a row in the listings table'''
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
            ret = {'id': listing.id}
            return jsonify(ret)
        except Exception as e:
            print 'ERROR: ', e 
            return makeError(400, str(e))
    else:
        return makeError(400, "listing json didn't validate")

@app.route('/api/listings', methods=['DELETE'])
def deleteListings():
    '''Delete all listings from the listings table'''
    try:
        models.Listing.query.delete()
        db.session.commit()
        return ('', 204) # no content
    except Exception as e:
        print 'ERROR: ', e 
        return makeError(400, str(e))

