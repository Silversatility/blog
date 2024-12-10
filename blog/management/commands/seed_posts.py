from django.core.management.base import BaseCommand
from blog.models import Author, Post
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Seed the database with test data for posts and authors"

    def handle(self, *args, **kwargs):
        author, created = Author.objects.get_or_create(
            name="John Doe",
            email="johndoe@example.com",
        )
        if created:
            self.stdout.write(f"Created author: {author.name} ({author.email})")
        else:
            self.stdout.write(f"Author already exists: {author.name} ({author.email})")

        post, created = Post.objects.get_or_create(
            title="Sample Blog Post",
            content="This is a sample blog post content.",
            published_date=now(),
            author=author,
            status="published",
        )
        if created:
            self.stdout.write(f"Created post: {post.title}")
        else:
            self.stdout.write(f"Post already exists: {post.title}")
