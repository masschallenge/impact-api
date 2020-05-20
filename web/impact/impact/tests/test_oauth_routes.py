# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from oauth2_provider.models import get_application_model
from test_plus.test import TestCase
from .factories import UserFactory

# pylint: disable=invalid-name
OAuth_App = get_application_model()


class TestOAuthRoutes(TestCase):
    user_factory = UserFactory

    def test_application_display(self):
        basic_user = self.make_user("basic_user@test.com")
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Test333",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired("oauth2_provider:list")
        self.assertLoginRequired("oauth2_provider:detail", pk=app.pk)

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:list")
            self.assertResponseContains("Test333", html=False)
            self.get_check_200("oauth2_provider:detail", pk=app.pk)
            self.assertResponseContains("Test333", html=False)

    def test_application_creation_workflow(self):
        basic_user = self.make_user("basic_user@test.com")

        self.assertLoginRequired("oauth2_provider:register")

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:register")
            form_data = {
                "name": "Test888",
                "client_id": "client_id",
                "client_secret": "client_secret",
                "client_type": OAuth_App.CLIENT_PUBLIC,
                "redirect_uris": "http://example.com",
                "authorization_grant_type": OAuth_App.GRANT_PASSWORD
            }
            self.post("oauth2_provider:register", data=form_data)
            self.response_302()
            self.assertTrue(OAuth_App.objects.filter(name="Test888").exists())
            self.get_check_200("oauth2_provider:list")
            self.assertResponseContains("Test888", html=False)
            app_pk = OAuth_App.objects.get(name="Test888").pk
            self.get_check_200("oauth2_provider:detail", pk=app_pk)

    def test_application_update_workflow(self):
        basic_user = self.make_user("basic_user@test.com")
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Test111",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired("oauth2_provider:update", pk=app.pk)

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:detail", pk=app.pk)
            self.assertResponseContains("Test111", html=False)
            self.get_check_200("oauth2_provider:update", pk=app.pk)
            form_data = {
                "user": basic_user.pk,
                "name": "Test222",
                "client_id": "client_id",
                "client_secret": "client_secret",
                "client_type": OAuth_App.CLIENT_PUBLIC,
                "redirect_uris": "http://example.com",
                "authorization_grant_type": OAuth_App.GRANT_PASSWORD
            }
            self.post("oauth2_provider:update", pk=app.pk, data=form_data)
            self.response_302()
            self.assertFalse(OAuth_App.objects.filter(name="Test111").exists())
            self.assertTrue(OAuth_App.objects.filter(name="Test222").exists())
            self.get_check_200("oauth2_provider:detail", pk=app.pk)
            self.assertResponseContains("Test222", html=False)
            self.assertResponseNotContains("Test111", html=False)

    def test_application_deletion(self):
        basic_user = self.make_user("basic_user@test.com")
        app = OAuth_App.objects.create(
            user=basic_user,
            name="Test555",
            client_type=OAuth_App.CLIENT_PUBLIC,
            authorization_grant_type=OAuth_App.GRANT_PASSWORD,
            redirect_uris="http://example.com",
        )

        self.assertLoginRequired("oauth2_provider:delete", pk=app.pk)

        with self.login(basic_user):
            self.get_check_200("oauth2_provider:detail", pk=app.pk)
            self.assertResponseContains("Test555", html=False)
            self.get_check_200("oauth2_provider:delete", pk=app.pk)
            self.post("oauth2_provider:delete", pk=app.pk)
            self.response_302()
            self.assertFalse(OAuth_App.objects.filter(pk=app.pk).exists())
            self.response_404(self.get("oauth2_provider:detail", pk=app.pk))
