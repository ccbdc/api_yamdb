from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.forms import ValidationError
from rest_framework import status, viewsets, permissions

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from api.filters import TitleFilter
from api.mixins import CategoryGenreMixinViewSet
from api.permissions import AdminOrReadOnly, AuthorStaffOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer)
from .models import Category, Genre, Title
from reviews.models import Review


codegen = PasswordResetTokenGenerator()


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = UserSerializer
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):

        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)

        return Response(serializer.data)


class SignupView(APIView):
    """
    The register a new user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, is_created = MyUser.objects.get_or_create(
            email=email,
            username=username
        )
        confirmation_code = codegen.make_token(user)
        mail_subject = 'Код подтверждения'
        message = f'Код подтверждения - {confirmation_code}'

        if is_created:
            user.is_active = False
            user.save()

        send_mail(
            mail_subject,
            message,
            settings.EMAIL_FROM,
            (email, )
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class TokenView(APIView):
    """
    Request a JWT-token.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GenTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(MyUser, username=username)

        if codegen.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': ['Код не действителен.']},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(ModelViewSet):
    """
    Processing a request to title.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist('genre')
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(
            category=category,
            genre=genres,
        )

    def perform_update(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist('genre')
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(
            category=category,
            genre=genres,
        )


class CategoryViewSet(CategoryGenreMixinViewSet):
    """
    Processing a request to category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixinViewSet):
    """
    Processing a request to genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_destroy(self, review):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(models.Title, id=title_id)
        user = self.request.user
        author = review.author
        if author == user:
            review = models.Review.objects.filter(title=title, author=self.request.user)
            title.rating = title.rating - review.score
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Удаление чужого контента запрещено')

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено')
        super(ReviewViewSet, self).perform_update(serializer)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorStaffOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
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