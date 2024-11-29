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

# Landing page
@app.route('/')
def home():
    return render_template('index.html')

# Increment page count and return
@app.route('/view/<int:item_id>', methods=['POST'])
def increment_view(item_id):
    try:
        page_view = PageView.query.filter_by(item_id=item_id).first()
        if not page_view:
            page_view = PageView(item_id=item_id, count=1)
            db.session.add(page_view)
        else:
            page_view.count += 1
        db.session.commit()
        return jsonify({"item_id": item_id, "count": page_view.count}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Could not process the request."}), 500

@app.route('/view/<int:item_id>', methods=['GET'])
def get_view_count(item_id):
    page_view = PageView.query.filter_by(item_id=item_id).first()
    if not page_view:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"item_id": item_id, "count": page_view.count}), 200

# Deletion route
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    try:
        # Attempt to delete the page view record for the item
        page_view = PageView.query.filter_by(item_id=item_id).first()
        if page_view:
            db.session.delete(page_view)  # Delete the page view record
            db.session.commit()
            return jsonify({"message": f"Item {item_id} deleted successfully."}), 200
        else:
            return jsonify({"error": f"Item {item_id} not found."}), 404
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({"error": f"Error deleting item: {e}"}), 500


# Add the reset route
# @app.route('/reset', methods=['POST'])
# def reset_database():
#     try:
#         # Delete all records from each table (including page_views)
#         PageView.query.delete()  # Deletes all entries from the page_views table
#         db.session.commit()  # Commit changes to the database
#         return 'Database has been reset successfully.', 200
#     except Exception as e:
#         return f'Error resetting database: {e}', 500

@app.route('/reset', methods=['POST', 'GET'])
def reset_database():
    if request.method == 'POST':
        try:
            # Delete all records from the page_views table
            PageView.query.delete()
            db.session.commit()
            # Return a success message with a "Back to Home" button
            return render_template('reset_success.html')  # Assuming reset_success.html displays the message and button
        except Exception as e:
            return f'Error resetting database: {e}', 500
    return render_template('reset_confirmation.html')  # Render reset confirmation page if GET request


if __name__ == '__main__':
    app.run(debug=True, port=5001)
