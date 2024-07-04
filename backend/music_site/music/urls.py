from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ArtistViewSet, SongViewSet, CommentViewSet, ActionViewSet, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'songs', SongViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'actions', ActionViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserViewSet.as_view({'get': 'list'}), name='profile'),
    path('songs/unapproved/', SongViewSet.as_view({'get': 'unapproved'}), name='unapproved-songs'),
    path('comments/unapproved/', CommentViewSet.as_view({'get': 'unapproved'}), name='unapproved-comments'),
    path('songs/hottest/', SongViewSet.as_view({'get': 'get_hottest_songs'}), name='hottest-songs'),
    path('songs/category/<int:category_id>/', SongViewSet.as_view({'get': 'get_songs_by_category'}), name='category-songs'),
    path('songs/artist/<int:artist_id>/', SongViewSet.as_view({'get': 'get_songs_by_artist'}), name='artist-songs'),
    path('songs/user/<int:user_id>/', SongViewSet.as_view({'get': 'get_songs_by_user'}), name='user-songs'),
    path('users/profile/likes-views/', UserViewSet.as_view({'get': 'profile_likes_views'}), name='profile-likes-views'),
]
