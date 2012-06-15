from django.test import TestCase
from django.contrib.auth.models import User


class HomePageTests(TestCase):

    fixtures = ['auth']

    def test_home_page_if_not_authenticated(self):

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_if_authenticated(self):

        self.client.login(
            username="danjac",
            password="test",
        )

        response = self.client.get("/")

        self.assertRedirects(response, "/dashboard/")


class DashboardTests(TestCase):

    fixtures = ['auth']

    def test_if_authenticated(self):

        self.client.login(
            username="danjac",
            password="test",
        )

        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_if_not_authenticated(self):

        response = self.client.get("/dashboard/")
        self.assertRedirects(response, "/account/login/?next=/dashboard/")



