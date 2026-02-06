students_db = []
id_tracker = 1

class Student:
    def __init__(self, first_name, last_name, grade, email):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.grade = grade
        self.email = email

    def save(self):
        global id_tracker
        
        self.id = id_tracker
        students_db.append(self)
        id_tracker += 1
        
        return self

    def to_dict(self):
        """Helper to convert the object to JSON-friendly dict"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "grade": self.grade,
            "email": self.email
        }