"""
apps.py

This module contains the configuration for the Posts application
                                                in the Django project.

The Posts application manages blog posts and comments,
                                        providing the necessary
models and configuration to handle user interactions and content moderation.

Classes:
    PostsConfig: Configuration class for the Posts application,
                                                specifying settings
                 related to the app's behavior and attributes.

Usage:
    You can include this configuration in your Django settings by adding
    'posts.apps.PostsConfig' to the INSTALLED_APPS list.
"""


from django.apps import AppConfig


class PostsConfig(AppConfig):

    """
    Configuration class for the Posts application.

    This class contains configuration settings for the Posts app, which handles
    the creation and management of blog posts and comments.

    Attributes:
        default_auto_field (str): The default type of auto-generated field for
                                  primary keys (BigAutoField).
        name (str): The name of the application, which is 'posts'.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
