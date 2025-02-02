from flask import Flask, request, redirect, url_for
from models.user import User
from extensions import db

def add_user_function():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    user = User(
        username=username,
        email=email,
        role=role
    )

    user.set_password(password)  # Postavi hashiranu lozinku pre čuvanja

    user.save()
    return redirect(url_for('home'))

def edit_user_function(data):
    data.username = request.form['username']
    data.email = request.form['email']
    data.password = request.form['password']
    data.role = request.form['role']

    db.session.commit()
    
    


def delete_user_function(user):
    db.session.delete(user)
    db.session.commit()