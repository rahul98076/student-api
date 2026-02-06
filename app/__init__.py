import logging
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from app.extensions import db, migrate
from app.models import Student

def create_app():

    load_dotenv()

    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    app.config.from_prefixed_env()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    print(f"DEBUG: Database URL is {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    migrate.init_app(app, db)


    @app.route('/healthcheck')
    def health_check():
        app.logger.info("Healthcheck endpoint called")
        return jsonify({"status": "ok"})


    @app.route('/api/v1/students', methods=['POST'])
    def create_student():
        data = request.get_json()
        new_student = Student(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            grade=data.get('grade'),
            email=data.get('email')
        )
        new_student.save()
        app.logger.info(f"Created new student with ID: {new_student.id}")
        return jsonify(new_student.to_dict()), 201


    @app.route('/api/v1/students', methods=['GET'])
    def get_students():
        app.logger.info("Fetching all students")
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])


    @app.route('/api/v1/students/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        app.logger.info(f"Fetching student ID: {student_id}")
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())


    @app.route('/api/v1/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        app.logger.info(f"Updating student ID: {student_id}")
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.grade = data.get('grade', student.grade)
        student.email = data.get('email', student.email)
        
        db.session.commit()
        return jsonify(student.to_dict())


    @app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        app.logger.info(f"Deleting student ID: {student_id}")
        student = Student.query.get_or_404(student_id)
        student.delete()
        return "", 204

    return app