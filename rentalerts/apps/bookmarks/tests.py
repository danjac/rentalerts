
from django.test import TestCase

from rentalerts.apps.bookmarks.models import Bookmark


class BookmarkListTests(TestCase):
    
    fixtures = ['auth', 'apartments']

    def setUp(self):

        bookmark = Bookmark.objects.create(
            apartment_id=1,
            user_id=3,
        )

    def test_if_not_authenticated(self):

        response = self.client.get("/bookmarks/")
        self.assertRedirects(response, "/account/login/?next=/bookmarks/")

    def test_if_authenticated(self):

        self.client.login(username="danjac", password="test")
        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 200)


class CreateBookmarkTests(TestCase):

    fixtures = ['auth', 'apartments']

    def test_if_not_authenticated(self):

        response = self.client.get("/bookmarks/3/create/")
        self.assertRedirects(response, "/account/login/?next=/bookmarks/3/create/")

    def test_if_authenticated(self):

        self.client.login(username="danjac", password="test")

        response = self.client.get("/bookmarks/3/create/")
        self.assertRedirects(response, "/apartments/3/", status_code=301)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_if_bookmark_already_created(self):
        
        Bookmark.objects.create(
            apartment_id=3,
            user_id=3,
        )


        self.client.login(username="danjac", password="test")
        
        response = self.client.get("/bookmarks/3/create/")
        self.assertRedirects(response, "/apartments/3/", status_code=301)
        self.assertEqual(Bookmark.objects.count(), 1)



class DeleteBookmarkTests(TestCase):

    fixtures = ['auth', 'apartments']

    def setUp(self):

        self.bookmark = Bookmark.objects.create(
            apartment_id=3,
            user_id=3,
        )

    def test_if_not_authenticated(self):

        response = self.client.get("/bookmarks/%s/delete/" % self.bookmark.id)
        self.assertRedirects(response, 
            "/account/login/?next=/bookmarks/%s/delete/" % self.bookmark.id)

    def test_if_not_bookmark_owner(self):

        self.client.login(username="weegill", password="test")

        response = self.client.get("/bookmarks/%s/delete/" % self.bookmark.id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_if_bookmark_owner(self):

        self.client.login(username="danjac", password="test")

        response = self.client.get("/bookmarks/%s/delete/" % self.bookmark.id)
        self.assertRedirects(response, "/apartments/3/", status_code=301)

        self.assertEqual(Bookmark.objects.count(), 0)

