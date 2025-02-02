from extensions import db
from sqlalchemy.dialects.mysql import ENUM
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(
        ENUM('user', 'admin', name='role_enum'),  
        nullable=False,
        default='user'  
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    def is_active(self):
        return True  

    def is_authenticated(self):
        return True  

    def is_anonymous(self):
        return False  

    def get_id(self):
        return str(self.id)  

    @property
    def data(self):
        return{
            'id': self.id,
            'username' : self.username,
            'email': self.email,
            'password': self.password_hash,
            'role' : self.role
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        r = cls.query.all()
        result = []

        for i in r:
            result.append(i.data)
        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()