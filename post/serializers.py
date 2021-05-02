from rest_framework import serializers

from blog.utils import get_default_error_messages
from user.serializers import ListUserSerializer
from post.models import Post


class PostBlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(error_messages=get_default_error_messages())
    content = serializers.CharField(error_messages=get_default_error_messages())

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'content')

    def create(self, validated_data):  # pylint: disable=R0912
        post = Post.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            user_id=self.user_id
        )
        return post


class EditPostBlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(error_messages=get_default_error_messages())
    content = serializers.CharField(error_messages=get_default_error_messages())
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'user_id')


class ListPostSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    class Meta:
        model = Post
        fields = '__all__'


class SearchPostSerializer(serializers.Serializer):
    q = serializers.CharField(allow_blank=True)
