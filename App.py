from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import time

# Flask app and DB configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bhuvan13@localhost/endpoint'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model
class Tb2_ResponseTime(db.Model):
    __tablename__ = 'Tb2_ResponseTime'

    Response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shortName = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    interval_time_second = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


# Create the table if it doesn’t exist
with app.app_context():
    db.create_all()


# Home route - render HTML page
@app.route('/')
def index():
    apps = Tb2_ResponseTime.query.all()
    return render_template('index.html', apps=apps)


# Add app endpoint
@app.route('/add', methods=['POST'])
def add_app():
    data = request.get_json()
    shortName = data.get('shortName')
    url = data.get('url')
    interval = data.get('interval')

    new_app = Tb2_ResponseTime(
        shortName=shortName,
        url=url,
        interval_time_second=interval,
        created_date=datetime.now()
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({'message': 'Application added successfully'})


# Get app list
@app.route('/get', methods=['GET'])
def get_apps():
    apps = Tb2_ResponseTime.query.all()
    result = []
    for app_row in apps:
        result.append({
            'Response_id': app_row.Response_id,
            'shortName': app_row.shortName,
            'url': app_row.url,
            'interval_time_second': app_row.interval_time_second,
            'status': app_row.status,
            'created_date': app_row.created_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(result)


# Delete an app by ID
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_app(id):
    app_row = Tb2_ResponseTime.query.get_or_404(id)
    db.session.delete(app_row)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'})


# Check status of URL
@app.route('/status/<int:id>')
def get_status(id):
    app_row = Tb2_ResponseTime.query.get_or_404(id)
    try:
        start = time.time()
        response = requests.get(app_row.url, timeout=5)
        end = time.time()
        response_time = round((end - start) * 1000)  # in ms

        return jsonify({
            "status": "Up" if response.ok else "Down",
            "response_time": f"{response_time} ms"
        })
    except Exception:
        return jsonify({
            "status": "Down",
            "response_time": "Timeout"
        })


if __name__ == '__main__':
    app.run(debug=True)
