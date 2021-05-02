import factory

from post.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
