from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Artist, Song, Comment, Action
from django.contrib.auth.models import User

class MusicAppTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password123')
        self.token = self.get_token_for_user('testuser', 'password123')
        self.admin_token = self.get_token_for_user('admin', 'password123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
        self.artist = Artist.objects.create(name='Test Artist')
        self.category = Category.objects.create(name='Rock')

    def get_token_for_user(self, username, password):
        url = reverse('login')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response.data['auth_token']

    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'password123', 'first_name': 'New', 'last_name': 'User'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        token = self.get_token_for_user('testuser', 'password123')
        self.assertIsNotNone(token)

    def test_get_logged_in_user_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_get_other_user_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url, {'id': self.admin_user.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin')

    def test_search_users(self):
        url = reverse('user-list')
        response = self.client.get(url, {'search': 'testuser'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_create_song(self):
        url = reverse('song-list')
        song_file = SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            'title': 'Test Song',
            'artist': self.artist.id,
            'category': self.category.id,
            'user': self.user.id,
            'file': song_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_song(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('song-detail', kwargs={'pk': song.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], song.title)

    def test_update_song(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('song-detail', kwargs={'pk': song.id})
        data = {'title': 'Updated Song'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Song')

    def test_delete_song(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('song-detail', kwargs={'pk': song.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_comment(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('comment-list')
        data = {'content': 'Great song!', 'song': song.id, 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_comment(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        comment = Comment.objects.create(content='Great song!', song=song, user=self.user, approved=True)
        url = reverse('comment-detail', kwargs={'pk': comment.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Great song!')

    # def test_admin_approve_song(self):
    #     self.client.login(username='admin', password='password123')
    #     song = Song.objects.create(
    #         title='Test Song',
    #         artist=self.artist,
    #         category=self.category,
    #         user=self.user,
    #         approved=False,
    #         file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
    #     )
    #     url = reverse('song-detail', kwargs={'pk': song.id})
    #     data = {'approved': True}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(response.data['approved'])

    # def test_admin_approve_comment(self):
    #     self.client.login(username='admin', password='password123')
    #     song = Song.objects.create(
    #         title='Test Song',
    #         artist=self.artist,
    #         category=self.category,
    #         user=self.user,
    #         approved=True,
    #         file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
    #     )
    #     comment = Comment.objects.create(content='Great song!', song=song, user=self.user, approved=False)
    #     url = reverse('comment-detail', kwargs={'pk': comment.id})
    #     data = {'approved': True}
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(response.data['approved'])

    def test_admin_block_song(self):
        self.client.login(username='admin', password='password123')
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('song-detail', kwargs={'pk': song.id})
        data = {'approved': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['approved'])

    def test_admin_remove_user_permissions(self):
        self.client.login(username='admin', password='password123')
        user_url = reverse('user-detail', kwargs={'pk': self.user.id})
        data = {'user_permissions': []}
        response = self.client.patch(user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.user_permissions.exists())

    def test_admin_get_unapproved_songs(self):
        Song.objects.create(
            title='Unapproved Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=False,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        Song.objects.create(
            title='Unapproved Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=False,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        url = reverse('song-unapproved')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_get_unapproved_comments(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        Comment.objects.create(content='Unapproved Comment 1', song=song, user=self.user, approved=False)
        Comment.objects.create(content='Unapproved Comment 2', song=song, user=self.user, approved=False)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        url = reverse('comment-unapproved')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_get_hottest_songs(self):
        Song.objects.create(
            title='Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=50,
            approved=True,
            file=SimpleUploadedFile("file1.mp3", b"file_content", content_type="audio/mpeg")
        )
        Song.objects.create(
            title='Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=100,
            approved=True,
            file=SimpleUploadedFile("file2.mp3", b"file_content", content_type="audio/mpeg")
        )
        Song.objects.create(
            title='Song 3',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=75,
            approved=True,
            file=SimpleUploadedFile("file3.mp3", b"file_content", content_type="audio/mpeg")
        )

        url = reverse('hottest-songs')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Song 2')  # Song 2 has the most likes
        self.assertEqual(response.data[1]['title'], 'Song 3')  # Song 3 has the second most likes
        self.assertEqual(response.data[2]['title'], 'Song 1')  # Song 1 has the third most likes
        
        
    def test_get_songs_by_category(self):
        song1 = Song.objects.create(
            title='Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            approved=True,
            file=SimpleUploadedFile("file1.mp3", b"file_content", content_type="audio/mpeg")
        )
        song2 = Song.objects.create(
            title='Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=5,
            approved=True,
            file=SimpleUploadedFile("file2.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('category-songs', kwargs={'category_id': self.category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_songs_by_artist(self):
        song1 = Song.objects.create(
            title='Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            approved=True,
            file=SimpleUploadedFile("file1.mp3", b"file_content", content_type="audio/mpeg")
        )
        song2 = Song.objects.create(
            title='Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=5,
            approved=True,
            file=SimpleUploadedFile("file2.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('artist-songs', kwargs={'artist_id': self.artist.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_songs_by_user(self):
        song1 = Song.objects.create(
            title='Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            approved=True,
            file=SimpleUploadedFile("file1.mp3", b"file_content", content_type="audio/mpeg")
        )
        song2 = Song.objects.create(
            title='Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=5,
            approved=True,
            file=SimpleUploadedFile("file2.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('user-songs', kwargs={'user_id': self.user.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_total_likes_and_views(self):
        Song.objects.create(
            title='Song 1',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            views=100,
            approved=True,
            file=SimpleUploadedFile("file1.mp3", b"file_content", content_type="audio/mpeg")
        )
        Song.objects.create(
            title='Song 2',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=20,
            views=200,
            approved=True,
            file=SimpleUploadedFile("file2.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('profile-likes-views')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_likes'], 30)
        self.assertEqual(response.data['total_views'], 300)
        
        
    def test_get_song_profile(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            views=100,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        url = reverse('song-profile', kwargs={'pk': song.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Song')

    def test_get_song_history(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            views=100,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )
        Action.objects.create(user=self.user, song=song, action_type='like')
        Action.objects.create(user=self.user, song=song, action_type='view')
        url = reverse('song-history', kwargs={'pk': song.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_crud_operations_on_song_by_uploader(self):
        song = Song.objects.create(
            title='Test Song',
            artist=self.artist,
            category=self.category,
            user=self.user,
            likes=10,
            views=100,
            approved=True,
            file=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        )

        # Update song
        url = reverse('song-detail', kwargs={'pk': song.id})
        data = {'title': 'Updated Song'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Song')

        # Delete song
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Song.objects.filter(id=song.id).exists())

    def test_crud_operations_on_category_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)

        # Create category
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Category')
        category_id = response.data['id']

        # Update category
        url = reverse('category-detail', kwargs={'pk': category_id})
        data = {'name': 'Updated Category'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')

        # Delete category
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category_id).exists())
