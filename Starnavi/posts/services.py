"""
JWT Authentication and Content Moderation Utilities

This module provides utilities for JSON Web Token (JWT) generation,
authentication, and content moderation in a Django application.

Functions:

create_jwt_token(user: User) -> str:
    Generates a JWT token for a given user, including user ID
    and an expiration time of 24 hours.

jwt_required(func: Callable) -> Callable:
    A decorator that protects views by requiring valid JWT
    authentication. It checks the request's Authorization header
    for a valid token and attaches the authenticated user
    to the request.

moderate_content(content: str) -> bool:
    Checks if the provided content contains inappropriate
    language by scanning it against a predefined list of
    profane words.

send_auto_reply(comment_id: int) -> None:
    Sends an automatic reply to a comment based on the
    associated post's settings. It checks if auto-replies
    are enabled for the post and waits for a specified
    delay before posting the reply.

Constants:

PROFANITY_LIST: A list of words considered inappropriate
  for content moderation.

Usage:

This module can be used in Django views to handle JWT
authentication and to moderate user-generated content.
Ensure that the necessary Django settings and models
are configured correctly.

"""

import jwt
import functools
from datetime import timedelta, timezone
from time import sleep
from typing import Callable, Any
from better_profanity import profanity

from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate

from posts.models import Comment


def create_jwt_token(user: User) -> str:

    """

    Generate a JWT token for the given user.

    This function creates a JSON Web Token (JWT) that includes the user's ID 
    and an expiration time set for 24 hours from the current time.

    Args:
        user: The user object for which the token is generated.

    Returns:
        str: The encoded JWT token.

    Raises:
        Exception: If there is an issue with encoding the token.

    """

    exp_time = timezone.now() + timedelta(days=1)

    payload: dict[str, Any] = {
        'user_id': user.id,
        'exp': exp_time,
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')



def jwt_required(func: Callable) -> Callable:

    """
    Decorator to protect views requiring JWT authentication.

    This decorator checks for a valid JWT in the request's 
    Authorization header. If the token is missing or invalid,
    it returns an error response. If the token is valid, it
    attaches the authenticated user to the request object.

    Args:
        func: The view function to be decorated.

    Returns:
        wrapper: A wrapped function that handles JWT verification.

    Raises:
        JsonResponse: Returns a 401 Unauthorized response if the token
                      is missing, expired, or invalid, or if the user
                      cannot be found.

    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if token is None:
            return JsonResponse({'error': 'Token is missing'}, status=401)

        try:
            payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
            request.user = User.objects.get(id=payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return func(request, *args, **kwargs)

    return wrapper


def moderate_content(content: str) -> bool:

    """
    Checks if the provided text contains profanity.

    This function uses the better-profanity library

    """

    profanity.load_censor_words()

    return profanity.contains_profanity(content)


def send_auto_reply(comment_id: int) -> None:

    """
    Send an automatic reply to a comment based 
                on the associated post's settings.

    This function retrieves the comment by its ID and checks if the
    associated post has automatic replies enabled. If enabled, it waits
    for the specified delay before creating a new comment as a reply
    using the auto-reply text from the post.

    Args:
        comment_id (int): The ID of the comment to which
                                    the reply will be sent.

    Raises:
        Comment.DoesNotExist: If the comment with the given ID does not exist.

    Usage:
        send_auto_reply(123)  # Sends an auto reply to the comment with ID 123.

    """

    comment = Comment.objects.get(id=comment_id)
    post = comment.post

    if post.auto_reply_enabled:
        sleep(post.auto_reply_delay)

        reply_content = post.auto_reply_text

        Comment.objects.create(
            post=post,
            author=post.author,
            content=reply_content
        )


def register_user(username: str, email: str, password: str) -> User:

    """

    Register a new user.

    Args:

        username (str): The desired username.
        email (str): The user's email address.
        password (str): The user's password.

    Returns:

        User: The created User instance.

    Raises:

        ValidationError: If the username or email already exists.

    """

    if User.objects.filter(username=username).exists():

        raise ValidationError("Username already exists.")

    if User.objects.filter(email=email).exists():

        raise ValidationError("Email already exists.")

    return User.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            )


def authenticate_user(username: str, password: str) -> User:

    """

    Authenticate a user by username and password.

    Args:

        username (str): The username of the user.
        password (str): The password of the user.

    Returns:

        User: The authenticated User instance.

    Raises:
        ValueError: If the credentials are invalid.
        ObjectDoesNotExist: If the user does not exist.

    """

    user = authenticate(username=username, password=password)

    if user is None:

        if not User.objects.filter(username=username).exists():

            raise ObjectDoesNotExist("User does not exist.")

        else:
            raise ValueError("Invalid password.")

    return user
