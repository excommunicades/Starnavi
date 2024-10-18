"""
Test suite for the blog post and comment API endpoints.

This module contains a series of tests to verify the functionality of
the API related to user registration, login, and operations involving
blog posts and comments. The tests utilize pytest and Django's test
client to ensure that the API behaves as expected.

Tests include:

1. User registration and login functionality.
2. Creation, moderation, and retrieval of blog posts.
3. Creation and listing of comments associated with posts.
4. Automatic reply functionality triggered by comments.
5. Daily breakdown of comments, including counts of total and blocked comments.

Each test is marked with @pytest.mark.django_db to allow for database
interactions, and the auth_client fixture is used for tests requiring
authentication.

Usage:

    To run the tests, use the following command:

    pytest path/to/this_file.py

Dependencies:
    Django
    pytest
    pytest-django

Fixtures:
    auth_client: Provides an authenticated client for testing API endpoints
                                        that require user authentication.

"""

import pytest
import json
import time

from django.conf import settings
from django.contrib.auth.models import User

from posts.models import Post, Comment


@pytest.fixture
def auth_client(client):

    """

    Fixture to create an authenticated client for testing.

    This fixture creates a new user, logs in to obtain a JWT token, and
    configures the client to include the token in its authorization header
    for subsequent requests.

    Steps:

        1. Create a user with a predefined username, password, and email.
        2. Log in with the created user's credentials to receive a JWT token.
        3. Assert that the login request is successful (status code 200).
        4. Ensure that a token is returned.
        5. Set the authorization header for the client with the obtained token.

    Args:

        client: A pytest fixture that provides a standard Django test client.

    Returns:

        client: The authenticated client configured with
                                    the JWT token for further requests.

    Usage:

        In tests that require authentication, you can use
                                    the `auth_client` fixture:

        def test_some_protected_view(auth_client):
            response = auth_client.get("/api/protected-view/")
            assert response.status_code == 200

    """

    User.objects.create_user(
                        username='testuser',
                        password='password123',
                        email='test@example.com',
                        )

    url = "/api/login/"

    data = {
        'username': 'testuser',
        'password': 'password123',
    }

    response = client.post(
                        url, json.dumps(data),
                        content_type='application/json',
                        )

    token = response.json().get('token')

    assert response.status_code == 200

    assert token is not None

    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'


@pytest.mark.django_db
def test_register_user(client):

    """
    Test the user registration functionality.

    This test verifies that a new user can register successfully
    through the API
    and receives a user ID in the response.

    Steps:

        1. Define the API endpoint for user registration.
        2. Prepare the registration data including username,
                                                email, and password.

        3. Send a POST request to the registration endpoint.
        4. Assert that the response status code is 201 (Created).

        5. Verify that the response contains an 'id',
        indicating successful registration.

    Args:

        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the registration request
                                            has a status code of 201.

        Asserts that the response includes an 'id', confirming
        successful user creation.
    """

    url = "/api/register/"

    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
    }

    response = client.post(
                        url,
                        data=json.dumps(data),
                        content_type='application/json',
                        )

    assert response.status_code == 201

    assert 'id' in response.json()

    response_duplicate = client.post(
        url,
        data=json.dumps(data),
        content_type='application/json',
    )

    assert response_duplicate.status_code == 400

    assert 'error' in response_duplicate.json()


@pytest.mark.django_db
def test_login_user(client):

    """

    Test the user login functionality.

    This test verifies that a user can log in successfully through the API
    and receives a JWT token in the response.

    Steps:

        1. Create a test user with a username, password, and email.
        2. Define the API endpoint for user login.
        3. Prepare the login data with the user's credentials.
        4. Send a POST request to the login endpoint.
        5. Assert that the response status code is 200 (OK).
        6. Verify that the response contains a 'token',
        indicating successful login.

    Args:

        client: A pytest fixture for standard client requests.

    Asserts:

        -Asserts that the response from the login request
                                        has a status code of 200.

        Asserts that the response includes a 'token', confirming
        successful authentication.

    """

    User.objects.create_user(
                    username='testuser',
                    password='password123',
                    email='test@example.com',
                    )

    url = "/api/login/"

    data = {
        'username': 'testuser',
        'password': 'password123',
    }

    response = client.post(
                        url,
                        data,
                        content_type='application/json',
                        )

    assert response.status_code == 200

    assert 'token' in response.json()


@pytest.mark.django_db
def test_create_post(auth_client, client):

    """
    Test the creation of a new blog post.

    This test verifies that a new blog post can be successfully created
    via the API and that the response contains the expected data.

    Steps:

        1. Define the API endpoint for creating a new post.
        2. Prepare the post data with title, content, and auto-reply settings.
        3. Send a POST request to create the post.
        4. Assert that the response status code is 201 (created).
        5. Verify that the response contains an 'id' field,
        indicating successful creation.

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the post creation
                                        has a status code of 201.

        Asserts that the response includes an 'id', confirming
        that the post was created.
    """

    url = "/api/posts/"

    data = {
        'title': 'Test Post',
        'content': 'This is a test post.',
        'auto_reply_enabled': False,
        'auto_reply_delay': 0,
        'auto_reply_text': '',
    }

    response = client.post(
                        url,
                        data=json.dumps(data),
                        content_type='application/json',
                        )

    assert response.status_code == 201

    assert 'id' in response.json()


@pytest.mark.django_db
def test_moderate_content(auth_client, client):

    """

    Test the content moderation functionality when creating a new post.

    This test verifies that when a post is created with inappropriate
    language in its content, the post is marked as blocked.

    Steps:

        1. Define the API endpoint for creating a new post.
        2. Prepare the post data, including inappropriate content ("fuck").
        3. Send a POST request to create the post.
        4. Assert that the response status code is 201 (created).
        5. Verify that the response contains an 'id' field.
        6. Assert that the post is marked as blocked (is_blocked is True).

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the post creation
                                        has a status code of 201.

        Asserts that the response includes an 'id' indicating
                                            successful creation.

        Asserts that the post is flagged as blocked due
        to inappropriate content.

    """

    url = "/api/posts/"
    data = {
        'title': 'Test Post',
        'content': 'fuck ',
        'auto_reply_enabled': False,
        'auto_reply_delay': 0,
        'auto_reply_text': '',
    }
    response = client.post(
                        url,
                        data=json.dumps(data),
                        content_type='application/json',
                        )

    assert response.status_code == 201

    assert 'id' in response.json()

    assert response.json()['is_blocked'] is True


@pytest.mark.usefixtures("transactional_db")
def test_send_auto_reply(auth_client, client):

    """

    Test the automatic reply functionality when a comment is made on a post.

    This test verifies that when a comment is added to a blog post with
    automatic replies enabled, the system responds with an automatic
    reply after a specified delay.

    Steps:
        1. Create a new blog post with auto-reply settings.
        2. Assert that the post creation is successful (status code 201).
        3. Create a comment for the newly created post.
        4. Assert that the comment creation is successful (status code 201).
        5. Verify that the comment exists in the database.
        6. Wait for the auto-reply delay period to elapse.
        7. Check that an automatic reply comment has been
        created with the expected content.

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the post creation
                                    has a status code of 201.

        Asserts that the response from the comment creation
                                    has a status code of 201.

        Asserts that the comment exists in the database.
        Asserts that one auto-reply comment has been created
        with the specified content.
    
    """

    post_url = "/api/posts/"

    post_data = {
        'title': 'Test Post',
        'content': 'This is a test post.',
        'auto_reply_enabled': True,
        'auto_reply_delay': 1,
        'auto_reply_text': 'Thank you for your comment!',
    }

    post_response = client.post(
                            post_url, 
                            data=json.dumps(post_data),
                            content_type='application/json',
                            )

    assert post_response.status_code == 201

    post_id = post_response.json()['id']

    comment_url = f"/api/posts/{post_id}/comments/"

    comment_data = {
        'content': 'This is a test comment.'
    }

    comment_response = client.post(
                                comment_url,
                                data=json.dumps(comment_data),
                                content_type='application/json',
                                )

    assert comment_response.status_code == 201

    comment_id = comment_response.json()['id']

    assert Comment.objects.filter(id=comment_id).exists()

    time.sleep(2.0)

    auto_reply_count = Comment.objects.filter(
                                        post_id=post_id,
                                        content='Thank you for your comment!',
                                        ).count()

    assert auto_reply_count == 1


@pytest.mark.django_db
def test_create_comment(auth_client, client):

    """

    Test the create comment API endpoint.

    This test verifies that a new comment can be successfully created
    for a specific blog post. It checks that the response returns the
    expected status code and that the created comment's ID is present
    in the response.

    Steps:

        1. Retrieve a test user from the database.
        2. Create a test post authored by the user.
        3. Make a POST request to the comments endpoint for the created post.
        4. Assert that the response status code is 201,
                        indicating successful creation.

        5. Assert that the response includes the 'id' of
        the newly created comment.

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the endpoint has a status code of 201
        and that the response contains an 'id' key, indicating
        the comment was created.

    """

    user = User.objects.get(username='testuser')

    post = Post.objects.create(
                            title='Test Post',
                            content='This is a test post.',
                            author=user,
                            )

    url = f"/api/posts/{post.id}/comments/"

    data = {
        'content': 'This is a test comment.'
    }

    response = client.post(
                        url,
                        data,
                        content_type='application/json',
                        )

    assert response.status_code == 201

    assert 'id' in response.json()


@pytest.mark.django_db
def test_list_posts(auth_client, client):

    """
    Test the list posts API endpoint.

    This test verifies that all blog posts created by a user are correctly
    retrieved through the API. It checks that the response returns the
    expected number of posts.

    Steps:

        1. Retrieve a test user from the database.
        2. Create two posts authored by the test user.
        3. Make a GET request to the posts endpoint.
        4. Assert that the response status code is 200, indicating success.
        5. Assert that the number of posts returned matches the expected count.

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the endpoint has a status code of 200
        and that the number of posts returned is 2.

    """

    user = User.objects.get(username='testuser')

    Post.objects.create(
                    title='Post 1',
                    content='Content 1',
                    author=user,
                    )

    Post.objects.create(
                    title='Post 2',
                    content='Content 2',
                    author=user,
                    )

    url = "/api/posts/"

    response = client.get(
                        url,
                        content_type='application/json',
                        )

    assert response.status_code == 200

    assert len(response.json()) == 2


@pytest.mark.django_db
def test_list_comments(auth_client, client):

    """
    Test the list comments API endpoint for a specific post.

    This test verifies that the comments associated with a given post are 
    correctly retrieved through the API. It checks that the response returns
    the expected number of comments.

    Steps:

        1. Retrieve a test user from the database.
        2. Create a test post authored by the test user.
        3. Create two comments for the post.
        4. Make a GET request to the comments endpoint for the created post.
        5. Assert that the response status code is 200, indicating success.
        6. Assert that the number of comments returned matches
        the expected count.

    Args:

        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:

        Asserts that the response from the endpoint has a status code of 200
        and that the number of comments returned is 2.

    """

    user = User.objects.get(username='testuser')

    post = Post.objects.create(
                            title='Test Post',
                            content='This is a test post.',
                            author=user,
                            )

    Comment.objects.create(
                        post=post,
                        author=user,
                        content='First comment.',
                        )

    Comment.objects.create(
                        post=post,
                        author=user,
                        content='Second comment.',
                        )

    url = f"/api/posts/{post.id}/comments/"

    response = client.get(
                        url,
                        content_type='application/json',
                        )

    assert response.status_code == 200

    assert len(response.json()) == 2


@pytest.mark.django_db
def test_comments_daily_breakdown(auth_client, client):

    """

    Test the comments_daily_breakdown API endpoint.

    This test checks the functionality of
    the comments_daily_breakdown endpoint,

    ensuring it returns the correct counts of total and blocked comments within
    a specified date range.

    Steps:

        1. Retrieve a test user from the database.
        2. Create a test post authored by the test user.
        3. Create two comments for the post, one of which is blocked.
        4. Make a GET request to the comments_daily_breakdown endpoint
                                                    with a date range.

        5. Assert that the response status code is 200, indicating success.

    Args:
        auth_client: A pytest fixture for authenticated client requests.
        client: A pytest fixture for standard client requests.

    Asserts:
        Asserts that the response from the endpoint has a status code of 200.

    """

    user = User.objects.get(username='testuser')

    post = Post.objects.create(
                            title='Test Post',
                            content='This is a test post.',
                            author=user,
                            )

    Comment.objects.create(
                        post=post,
                        author=user,
                        content='First comment.',
                        )

    Comment.objects.create(
                        post=post,
                        author=user,
                        content='Second comment.',
                        is_blocked=True,
                        )

    url = "/api/comments-daily-breakdown/"

    response = client.get(
                        url,
                        {'date_from': '2024-01-01', 'date_to': '2024-12-31'},
                        content_type='application/json',
                        )

    assert response.status_code == 200
