import os
import logging
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    make_response
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import pytz 

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
logging.basicConfig(filename='request_log.txt', level=logging.DEBUG)

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(128), nullable=False, unique=True)
    organization_id = db.Column(db.Integer)
    order_id = db.Column(db.String(128), nullable=False)
    status_raw = db.Column(db.String(128), nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, 
                 ticket_id, 
                 order_id,
                 status_raw,
                 event_id,
                 date,
                 organization_id=0
                 ):
        self.ticket_id = ticket_id
        self.order_id = order_id
        self.status_raw = status_raw
        self.event_id = event_id
        self.date = date
        self.organization_id = organization_id

@app.route('/log', methods=['GET', 'POST'])
def log_request():
    # Log the details of the incoming request
    data = request.get_json()
    app.logger.info('Request received: %s %s. Data: %s', request.method, request.path, data.dump())
    str_timestamp = data['hook_generated_at']
    # Parse the string into a datetime object with time zone information
    dt = pytz.timezone("UTC").localize(datetime.strptime(str_timestamp, "%Y-%m-%d %H: %M: %S"))
    dataset = db.session.execute(db.select(Ticket).filter_by(ticket_id = data['id'])).scalars()
    dataset_len = len(dataset.all())
    app.logger.info(dataset_len)
    if dataset_len == 0:
        db.session.add(Ticket(ticket_id=data['id'],
                            order_id=data['order_id'],
                            status_raw=data['status_raw'],
                            event_id=data['event_id'],
                            date=dt,
                            organization_id=data['organization_id']))
        db.session.commit()
        
        return make_response('Logged', 200)
    else:
        return make_response('Not logged', 200)
