"""
admin.py

This module is used to register the Post and Comment
models with the Django admin site,
allowing for easy management of blog posts and comments
through the admin interface.

Models Registered:
    Post: Represents a blog post, including its title, content,
                                        author, and other attributes.
                         
    Comment: Represents a comment associated with a blog post,
                        including its content, author, and blocking status.

Usage:
    After registering, these models can be managed through
                                        the Django admin interface.

    Make sure to run the server and access the admin site at /admin/
                                    to view and edit posts and comments.
"""


from django.contrib import admin

from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
