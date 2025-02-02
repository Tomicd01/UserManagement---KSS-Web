from extensions import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer,  db.ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    @property
    def data(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return [order.data for order in cls.query.all()]

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
