from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.response import Response

from post.models import Post
from post.serializers import (EditPostBlogSerializer, ListPostSerializer,
                              PostBlogSerializer, SearchPostSerializer)


class PostViewSet(viewsets.ViewSet):
    def post(self, request):
        post_serializer = PostBlogSerializer(data=request.data, user_id=request.user.user.id)
        post_serializer.is_valid(raise_exception=True)

        post_serializer.save()
        return Response(post_serializer.data, status.HTTP_201_CREATED)

    def list(self, request):
        post = Post.objects.all()
        list_post_serializer = ListPostSerializer(post, many=True)
        return Response(list_post_serializer.data, status.HTTP_200_OK)

    def get_post(self, request, pk):
        post = Post.objects.filter(id=pk)
        if not post.exists():
            return Response({'message': 'Post não existe'}, status.HTTP_404_NOT_FOUND)

        post_serializer = ListPostSerializer(post[0])
        return Response(post_serializer.data, status.HTTP_200_OK)

    def delete_post(self, request, pk):
        post = Post.objects.filter(id=pk)
        if not post.exists():
            return Response({'message': 'Post não existe'}, status.HTTP_404_NOT_FOUND)

        if post.exists() and post[0].user_id != request.user.user.id:
            return Response({'message': 'Usuário não autorizado'}, status.HTTP_401_UNAUTHORIZED)

        post[0].delete()
        return Response({}, status.HTTP_204_NO_CONTENT)

    def edit_post(self, request, pk):
        post = Post.objects.filter(id=pk)

        if not post.exists():
            return Response({'message': 'Post não existe'}, status.HTTP_404_NOT_FOUND)

        if post.exists() and post[0].user_id != request.user.user.id:
            return Response({'message': 'Usuário não autorizado'}, status.HTTP_401_UNAUTHORIZED)

        post_serializer = EditPostBlogSerializer(post[0], data=request.data)
        post_serializer.is_valid(raise_exception=True)

        post_serializer.save()
        return Response(post_serializer.data, status.HTTP_200_OK)

    def search(self, request):
        search_serializer = SearchPostSerializer(data=request.query_params)
        search_serializer.is_valid(raise_exception=True)

        post = Post.objects.filter(
            Q(title__contains=search_serializer.validated_data['q']) | Q(
                content__contains=search_serializer.validated_data['q']))
        list_post_serializer = ListPostSerializer(post, many=True)
        return Response(list_post_serializer.data, status.HTTP_200_OK)
