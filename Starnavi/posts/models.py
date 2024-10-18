"""

Models for a blog application, including posts and comments.

This module defines the following models:

Post: Represents a blog post.
Comment: Represents a comment on a post.

"""

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    """
    Model representing a blog post.

    Fields:

        title (str): The title of the post.
        content (str): The content of the post.
        author (User): The author of the post (foreign key to the User model).
        created_at (datetime): The date and time when the post was created.

        is_blocked (bool): Indicates whether the post
                                is blocked (default is False).

        auto_reply_enabled (bool): Flag to indicate if auto-reply
                                is enabled (default is False).

        auto_reply_delay (int): Delay in seconds before sending
                                an auto-reply (default is 0).
        auto_reply_text (str): Text for the auto-reply; can be blank or null.

    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    auto_reply_enabled = models.BooleanField(default=False)
    auto_reply_delay = models.IntegerField(default=0)
    auto_reply_text = models.TextField(blank=True, null=True)

    def __str__(self):

        """Return a string representation of the post."""

        return self.title


class Comment(models.Model):

    """
    Model representing a comment on a post.

    Fields:

        post (Post): The post to which the comment belongs
                                (foreign key to the Post model).

        content (str): The content of the comment.

        author (User): The author of the comment
                                (foreign key to the User model).

        created_at (datetime): The date and time when the comment was created.

        is_blocked (bool): Indicates whether the comment
                                is blocked (default is False).
    """

    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)

    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
