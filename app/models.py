from app import db

# Define the PageView model
class PageView(db.Model):
    __tablename__ = 'page_views'
    
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment ID
    item_id = db.Column(db.Integer, unique=True, nullable=False)  # Unique integer identifier for the item
    count = db.Column(db.Integer, nullable=False, default=0)  # View count
    
    def __repr__(self):
        return f"<PageView(item_id={self.item_id}, count={self.count})>"
