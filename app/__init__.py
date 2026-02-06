import logging
from flask import Flask, jsonify, request
from app.models import Student, students_db

def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)

    app.config.from_prefixed_env()


    @app.route('/healthcheck')
    def health_check():
        app.logger.info("Healthcheck endpoint called")
        return jsonify({"status": "ok"})


    @app.route('/api/v1/students', methods=['POST'])
    def create_student():
        data = request.get_json()
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        grade = data.get('grade')
        email = data.get('email')

        new_student = Student(first_name, last_name, grade, email)
        new_student.save()
        
        app.logger.info(f"Created new student with ID: {new_student.id}")

        return jsonify(new_student.to_dict()), 201


    @app.route('/api/v1/students', methods=['GET'])
    def get_students():
        app.logger.info("Fetching all students")
        student_list = []
        for student in students_db:
            student_list.append(student.to_dict())
        return jsonify(student_list)


    @app.route('/api/v1/students/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        app.logger.info(f"Fetching student ID: {student_id}")
        for student in students_db:
            if student.id == student_id:
                return jsonify(student.to_dict())
        
        app.logger.warning(f"Student ID {student_id} not found")
        return jsonify({"error": "Student not found"}), 404


    @app.route('/api/v1/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        data = request.get_json()
        app.logger.info(f"Updating student ID: {student_id}")
        
        for student in students_db:
            if student.id == student_id:
                student.first_name = data.get('first_name', student.first_name)
                student.last_name = data.get('last_name', student.last_name)
                student.grade = data.get('grade', student.grade)
                student.email = data.get('email', student.email)
                
                return jsonify(student.to_dict())
        
        return jsonify({"error": "Student not found"}), 404


    @app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        app.logger.info(f"Deleting student ID: {student_id}")
        for student in students_db:
            if student.id == student_id:
                students_db.remove(student)
                return "", 204
        
        return jsonify({"error": "Student not found"}), 404

    return app