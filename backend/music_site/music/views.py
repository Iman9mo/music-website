from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Category, Artist, Song, Comment, Action
from .serializers import CategorySerializer, ArtistSerializer, SongSerializer, CommentSerializer, ActionSerializer, UserSerializer, RegisterSerializer
from rest_framework import viewsets, generics, permissions, filters
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .permissions import IsOwnerOrReadOnly
from django.core.exceptions import PermissionDenied
from django.utils.dateparse import parse_date



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAdminUser]

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def unapproved(self, request):
        unapproved_songs = Song.objects.filter(approved=False)
        serializer = self.get_serializer(unapproved_songs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='hottest', url_name='hottest')
    def get_hottest_songs(self, request):
        top_songs = Song.objects.filter(approved=True).order_by('-likes')[:10]
        serializer = self.get_serializer(top_songs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)', url_name='category-songs')
    def get_songs_by_category(self, request, category_id=None):
        songs = Song.objects.filter(category_id=category_id, approved=True)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='artist/(?P<artist_id>[^/.]+)', url_name='artist-songs')
    def get_songs_by_artist(self, request, artist_id=None):
        songs = Song.objects.filter(artist_id=artist_id, approved=True)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)', url_name='user-songs')
    def get_songs_by_user(self, request, user_id=None):
        songs = Song.objects.filter(user_id=user_id, approved=True)
        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-period', url_name='songs-by-period')
    def get_songs_by_period(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Please provide both start_date and end_date in the format YYYY-MM-DD."}, status=400)

        try:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
        except ValueError:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

        if start_date > end_date:
            return Response({"error": "start_date must be before end_date."}, status=400)

        songs = Song.objects.filter(created_at__range=(start_date, end_date))
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
    @action(detail=True, methods=['get'], url_path='profile', url_name='song-profile')
    def get_song_profile(self, request, pk=None):
        song = self.get_object()
        serializer = self.get_serializer(song)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='history', url_name='song-history')
    def get_song_history(self, request, pk=None):
        song = self.get_object()
        actions = Action.objects.filter(song=song, user=request.user)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to edit this song')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('You do not have permission to delete this song')
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def unapproved(self, request):
        unapproved_comments = Comment.objects.filter(approved=False)
        serializer = self.get_serializer(unapproved_comments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    @action(detail=False, methods=['get'], url_path='profile', url_name='profile')
    def profile(self, request):
        user_id = request.query_params.get('id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
    @action(detail=False, methods=['get'], url_path='profile/likes-views', url_name='profile-likes-views')
    def profile_likes_views(self, request):
        user = request.user
        songs = Song.objects.filter(user=user)
        total_likes = songs.aggregate(Sum('likes'))['likes__sum'] or 0
        total_views = songs.aggregate(Sum('views'))['views__sum'] or 0
        return Response({'total_likes': total_likes, 'total_views': total_views})
