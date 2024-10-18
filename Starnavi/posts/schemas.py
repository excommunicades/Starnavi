"""

Schemas for Blog and User Management

This module defines schemas used for validating and serializing input
and output data related to blog posts, comments, and user management
in a Django application. The schemas are implemented using Pydantic
through the Ninja framework, providing strong type checking and data
validation.

Classes:

PostIn:
    Schema for input data when creating a new blog post. It includes
    fields for title, content, and optional auto-reply settings.

PostOut:
    Schema for output data representing a blog post. It includes
    fields for the post's ID, title, content, and creation timestamp.

CommentIn:
    Schema for input data when creating a new comment. It contains
    the content of the comment.

CommentOut:
    Schema for output data representing a comment. It includes fields
    for the comment's ID, associated post ID, content, author ID,
    creation timestamp, and a flag indicating whether the comment
    is blocked.

UserRegistration:
    Schema for input data when registering a new user. It includes
    fields for username, password, and email.

UserResponse:
    Schema for output data after user registration. It contains fields
    for the user's ID, username, and email.

UserLogin:
    Schema for input data when a user logs in. It includes fields
    for username and password.

Token:
    Schema for output data representing a JWT token used for user
    authentication.

Usage:
These schemas can be used in API endpoints to validate incoming
requests and format outgoing responses, ensuring that the data
conforms to expected types and structures.

"""

from ninja import Schema, Field
from datetime import datetime
from pydantic import BaseModel, Field, constr, EmailStr


class PostIn(Schema):

    """
    Schema for input data when creating a new blog post.

    Attributes:
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    """

    title: constr(min_length=1)
    content: constr(min_length=1)
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 0
    auto_reply_text: str = ""


class PostOut(Schema):

    """
    Schema for output data representing a blog post.

    Attributes:
        id (int): The unique identifier of the blog post.
        title (str): The title of the blog post.
        content (str): The content of the blog post.

    """

    id: int
    title: str
    content: str
    created_at: datetime


class CommentIn(Schema):
    """
    Schema for input when creating a new comment.

    Attributes:
        content (str):The content of the comment to be added to the post.

    """
    content: str


class CommentOut(Schema):
    """
    Schema for output data representing a comment.

    Attributes:
        id (int): The unique identifier of the comment.
        post_id (int): The identifier of the post to which the comment belongs.
        content (str): The content of the comment.
        author_id (int): The identifier of the comment's author.
        created_at (str): The date and time when the comment was created,
                                            formatted as an ISO 8601 string.
        is_blocked (bool): Indicates whether
                            the comment is blocked (default is False).
    """

    id: int
    post_id: int
    content: str
    author_id: int
    created_at: str  # Убедитесь, что это строка
    is_blocked: bool

    @classmethod
    def from_orm(cls, obj):
        """
        Create an instance of CommentOut from a Django model instance.

        Args:
            cls: The class being created.
            obj: The Django model instance.

        Returns:
            CommentOut: The created instance with formatted created_at.
        """
        return cls(
            id=obj.id,
            post_id=obj.post.id,
            content=obj.content,
            author_id=obj.author.id,
            created_at=obj.created_at.isoformat(),
            is_blocked=obj.is_blocked
        )


class UserRegistration(Schema):

    """
    Schema for input data when registering a new user.

    Attributes:

        username (str): The username to be registered.
        password (str): The password for the new user.

    """

    username: constr(min_length=1)
    password: constr(min_length=6)
    email: EmailStr


class UserResponse(Schema):
    """
    Schema for output data after user registration.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the registered user.
    """

    id: int
    username: str
    email: str


class UserLogin(Schema):
    """
    Schema for input data when a user logs in.

    Attributes:

        username (str): The username for login.
        password (str): The password for login.

    """
    username: str
    password: str


class Token(Schema):

    """
    Schema for output data representing a token.

    Attributes:
        token (str): The JWT token used for user authentication.
    """

    token: str
