import pytest
from flask import url_for

def login(client, username, password):
    return client.post(
        '/auth/login',
        data=dict(username=username, password=password),
        follow_redirects=True
    )

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'We Did The Girl Math' in response.data

def test_login(client, test_user):
    response = login(client, 'testuser', 'password')
    assert response.status_code == 200
    assert b'Sign In' not in response.data  # No longer showing login button

def test_create_post(client, test_user):
    login(client, 'testuser', 'password')
    response = client.post(
        '/posts/create',
        data=dict(
            title='Test Post',
            expense='New bag',
            justification='It was 50% off so I basically made money',
            is_seeking_help=False
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Your post has been created!' in response.data