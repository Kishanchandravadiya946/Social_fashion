from flask import request, jsonify
from extensions import db
from models.site_user import SiteUser
from ..schemas.user_schema import UserSchema

class UserResource:
    @staticmethod
    def create_user():
     data = request.get_json()
     required_fields = ['username', 'email_address', 'password']
     for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
     phone_number = data.get('phone_number', None)

     new_user = SiteUser(
        username=data['username'],
        email_address=data['email_address'],
        phone_number=phone_number,
        password=data['password']  # Use hashing for production!
     )

     try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully!', 'user_id': new_user.id}), 201
     except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
     
    @staticmethod
    def login_user():
      data = request.get_json()
      required_fields = ['email_address', 'password']
    
      for field in required_fields:
         if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

      email_address = data['email_address']
      password = data['password']
      
      # console.write(email_address)
      user = SiteUser.query.filter_by(email_address=email_address).first()

      if not user:
         return jsonify({'error': 'User not found'}), 404

      if  (user.password!=password):
         return jsonify({'error': 'Invalid password'}), 401

      return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
   
    @staticmethod
    def get_users():
        users = SiteUser.query.all()
        userschema=UserSchema(many=True)
        return userschema.jsonify(users), 200
