#!env/bin/python
from app import app
app.run(debug=True, port=9090, host='0.0.0.0')
