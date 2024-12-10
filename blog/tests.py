import pytest
from rest_framework.test import APIClient
from .models import Author, Post, Comment
from django.utils.timezone import now

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def author():
    return Author.objects.create(name="John Doe", email="johndoe@example.com")

@pytest.fixture
def post(author):
    return Post.objects.create(
        title="Test Post",
        content="This is a test post.",
        published_date=now(),
        author=author,
        status="published",
    )

@pytest.fixture
def comment(post):
    return Comment.objects.create(post=post, content="This is a test comment.")


@pytest.mark.django_db
def test_post_list(api_client, post):
    response = api_client.get("/api/posts/")

    assert response.status_code == 200, "Expected status code 200 for post list"
    assert response.json(), "Expected non-empty response for published posts"
    assert response.json()['results'][0]["title"] == "Test Post", "Post title does not match"

    response = api_client.get("/api/posts/?search=Test")
    assert len(response.json()['results']) == 1, "Expected one post matching the title filter"

    response = api_client.get("/api/posts/?search=John")
    assert len(response.json()['results']) == 1, "Expected one post matching the author_name filter"


@pytest.mark.django_db
def test_create_post(api_client, author):
    data = {
        "title": "New Test Post",
        "content": "This is the content of the new post.",
        "published_date": now().isoformat(),
        "author": author.id,
    }
    response = api_client.post("/api/posts/create/", data, format="json")
    assert response.status_code == 201, "Expected status code 201 for post creation"
    assert Post.objects.filter(title="New Test Post").exists(), "Post was not created in the database"


@pytest.mark.django_db
def test_create_comment(api_client, post):
    data = {"content": "This is a new comment"}
    response = api_client.post(f"/api/posts/{post.id}/comments/", data=data)
    assert response.status_code == 201, "Expected status code 201 for comment creation"
    assert Comment.objects.filter(content="This is a new comment").exists(), "Comment was not created in the database"
