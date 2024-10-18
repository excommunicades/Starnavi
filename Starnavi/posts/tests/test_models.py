"""

Tests for Blog Application Models

This module contains unit tests for the Post and Comment models
in the blog application. It ensures that the models behave
as expected, including their fields, relationships, and string
representations.

Tests:

1. test_post_creation: Verifies that a Post instance can be created
  successfully with valid data.

2. test_comment_creation: Checks that a Comment instance can be
  created successfully with valid data.

3. test_post_string_representation: Ensures that the string
  representation of a Post instance returns the title.

4. test_comment_relationship: Validates the relationship between
  Comment and Post models by checking if comments are linked
  correctly to their posts.

"""

import pytest

from django.contrib.auth.models import User

from posts.models import Post, Comment


@pytest.mark.django_db
def test_post_creation():

    """

    Test the creation of a Post instance.

    This test verifies that a Post can be created successfully
    with valid data and checks if the attributes are set correctly.

    """
    user = User.objects.create_user(
                            username='author',
                            password='testpass',
                            )

    post = Post.objects.create(
        title='Test Post',
        content='This is a test post.',
        author=user,
        auto_reply_enabled=True,
        auto_reply_delay=5,
        auto_reply_text='Thank you for your comment!',
    )

    assert post.title == 'Test Post'

    assert post.content == 'This is a test post.'

    assert post.author == user

    assert post.auto_reply_enabled is True

    assert post.auto_reply_delay == 5

    assert post.auto_reply_text == 'Thank you for your comment!'

    assert post.is_blocked is False


@pytest.mark.django_db
def test_comment_creation():

    """

    Test the creation of a Comment instance.

    This test verifies that a Comment can be created successfully
    with valid data and checks if the attributes are set correctly.

    """

    user = User.objects.create_user(
                            username='author',
                            password='testpass',
                            )

    post = Post.objects.create(
                        title='Test Post',
                        content='This is a test post.',
                        author=user,
                        )

    comment = Comment.objects.create(
        post=post,
        content='This is a test comment.',
        author=user
    )

    assert comment.content == 'This is a test comment.'

    assert comment.post == post

    assert comment.author == user

    assert comment.is_blocked is False


@pytest.mark.django_db
def test_post_string_representation():

    """

    Test the string representation of a Post instance.

    This test verifies that the __str__ method of the Post model
    returns the correct title of the post.

    """

    user = User.objects.create_user(username='author', password='testpass')

    post = Post.objects.create(
                        title='Test Post',
                        content='This is a test post.',
                        author=user,
                        )

    assert str(post) == 'Test Post'


@pytest.mark.django_db
def test_comment_relationship():

    """

    Test the relationship between Comment and Post models.

    This test checks that comments are correctly linked to their
    respective posts and that the related_name functionality works.

    """

    user = User.objects.create_user(
                        username='author',
                        password='testpass',
                        )

    post = Post.objects.create(
                        title='Test Post',
                        content='This is a test post.',
                        author=user,
                        )

    comment = Comment.objects.create(
                            post=post,
                            content='This is a test comment.',
                            author=user,
                            )

    assert comment.post == post

    assert post.comments.count() == 1

    assert post.comments.first() == comment
