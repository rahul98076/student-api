def test_create_student(client):
    response = client.post('/api/v1/students', json={
        "first_name": "Test",
        "last_name": "User",
        "grade": "A",
        "email": "test@test.com"
    })
    
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['email'] == "test@test.com"
    assert 'id' in data

def test_get_students(client):
    client.post('/api/v1/students', json={
        "first_name": "Existing", 
        "last_name": "Student", 
        "grade": "B", 
        "email": "exist@test.com"
    })

    response = client.get('/api/v1/students')
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['first_name'] == "Existing"