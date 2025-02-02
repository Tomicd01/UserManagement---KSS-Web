from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user import User  

def admin_required(f):
    @wraps(f)
    @jwt_required() 
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()  #  Dobijamo ID korisnika iz tokena
        user = User.get_by_id(user_id)  #  Učitavamo korisnika iz baze
        
        if not user or user.role != "admin":  # ✅ Proveravamo da li korisnik ima rolu admin
            return jsonify({"message": "Unauthorized: Admins only!"}), 403  

        return f(*args, **kwargs)  # Ako je admin, poziva se originalna funkcija
    
    return decorated_function
