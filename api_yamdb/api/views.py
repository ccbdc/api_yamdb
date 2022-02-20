from rest_framework import viewsets
from reviews import models
from api import serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(models.Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_destroy(self, review):
        user = self.request.user
        author = review.author
        if author == user:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Удаление чужого контента запрещено')

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено')
        super(ReviewViewSet, self).perform_update(serializer)

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        new_queryset = models.Review.objects.filter(title_id=title)
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class =serializers.CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(models.Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, comment):
        user = self.request.user
        author = comment.author
        if author == user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Удаление чужого контента запрещено')

    def get_queryset(self):
        review = self.kwargs.get('review_id')
        new_queryset = models.Comment.objects.filter(review_id=review)
        return new_queryset
