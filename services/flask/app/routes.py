from datetime import datetime as dt
from flask import current_app as app, request, make_response, jsonify
from . import db
from sqlalchemy import text
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# SQL Query as a constant
QUERY_BOUNDING_BOX = """
    SELECT date_trunc('week', datetime) AS week,
           COUNT(*) AS average
    FROM raw_tripsdata 
    WHERE
        origin_coord && ST_MakeEnvelope (
        7.672837913286881, 44.9957109242058,
        10.07299025213017, 53.62044974829032,
        4326)
    GROUP BY date_trunc('week', datetime)
"""

@app.route('/', methods=['GET'])
def hello_world():
    try:
        results = []
        with db.engine.connect() as connection:
            result = connection.execute(text(QUERY_BOUNDING_BOX))
            for row in result:
                results.append({'week': row[0], 'average': row[1]})
        
        response = make_response(jsonify({'results': results}), 200)
        return response

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
        return response
