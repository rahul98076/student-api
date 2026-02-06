import pytest
from app import create_app, students_db

@pytest.fixture
def client():
    app = create_app()
    
    app.config['TESTING'] = True
   
    with app.test_client() as client:
        
        students_db.clear()
        
        yield client