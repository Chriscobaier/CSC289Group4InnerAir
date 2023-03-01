from inner_air import app


def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_login():
    response = app.test_client().get('/login')
    assert response.status_code == 200


def test_register():
    response = app.test_client().get('/register')
    assert response.status_code == 200
