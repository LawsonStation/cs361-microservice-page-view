from flask import Flask, request, jsonify, render_template
from app import db
from app.models import PageView
from sqlalchemy.exc import IntegrityError
import sqlite3

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///page_views.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Helper function to create or update an item
def create_or_update_item(item_id):
    try:
        page_view = PageView.query.filter_by(item_id=item_id).first()
        if not page_view:
            page_view = PageView(item_id=item_id, count=1)
            db.session.add(page_view)
        else:
            page_view.count += 1
        db.session.commit()
        return {"item_id": item_id, "count": page_view.count}, 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Could not process the request."}, 500

# Landing page
@app.route('/')
def home():
    page_views = PageView.query.all()  # Retrieve all records from the PageView table
    return render_template('index.html', page_views=page_views)

# Increment page count and return
@app.route('/view/<int:item_id>', methods=['POST'])
def increment_view(item_id):
    response, status_code = create_or_update_item(item_id)
    return jsonify(response), status_code

# Get view count and auto-create missing items
@app.route('/view/<int:item_id>', methods=['GET'])
def get_view_count(item_id):
    page_view = PageView.query.filter_by(item_id=item_id).first()
    if not page_view:
        # If no record exists, create one with an initial count of 1
        response, status_code = create_or_update_item(item_id)
        return jsonify(response), status_code
    else:
        # Increment count on every page view (even if the page is refreshed)
        page_view.count += 1
        db.session.commit()
        return jsonify({"item_id": item_id, "count": page_view.count}), 200

# Deletion route
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    try:
        page_view = PageView.query.filter_by(item_id=item_id).first()
        if page_view:
            db.session.delete(page_view)
            db.session.commit()
            return jsonify({"message": f"Item {item_id} deleted successfully."}), 200
        else:
            return jsonify({"error": f"Item {item_id} not found."}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error deleting item: {e}"}), 500

# Reset database route
@app.route('/reset', methods=['POST', 'GET'])
def reset_database():
    if request.method == 'POST':
        try:
            PageView.query.delete()
            db.session.commit()
            return render_template('reset_success.html')
        except Exception as e:
            return f'Error resetting database: {e}', 500
    return render_template('reset_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
