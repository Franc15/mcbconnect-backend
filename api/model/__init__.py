from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.String(20), primary_key=True)
    mcb_customer_id = db.Column(db.String(20), unique=True)

    def __init__(self, customer_id, mcb_customer_id):
        self.customer_id = customer_id
        self.mcb_customer_id = mcb_customer_id

    def __repr__(self):
        return '<Customer %r>' % self.customer_id