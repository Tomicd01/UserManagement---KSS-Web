from extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return [product.data for product in cls.query.all()]

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
