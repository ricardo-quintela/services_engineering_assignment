from django.contrib.auth.models import User, Group
from clinic.tests import BaseTestCase

from authentication.jwt import generate_token

class TestHtmlServing(BaseTestCase):
    """Tests access to the admin page
    """
    def setUp(self) -> None:
        super().setUp()
        admin = Group.objects.create(name="admin")

        self.admin = User.objects.create_user(username="admin", password="admin")
        self.admin.groups.set([admin])
        self.users.append(self.admin)

    def test_get_base_app_page(self):
        """tests if the rendered template is index.html
        """
        response = self.client.get("")
        self.assertTemplateUsed(
            response,
            "base.html"
        )

    def test_get_admin_app_page(self):
        """Tests if the admin page can be accessed by a user with admin role
        """
        self.client.cookies.load({"jwt": generate_token(self.admin)})
        response = self.client.get("/admin/")
        self.assertTemplateUsed(
            response,
            "admin.html"
        )

    def test_get_admin_app_page_no_perms(self):
        """Tests if the admin page's access is denied to a non admin user
        """
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get("/admin/")
        self.assertJSONEqual(
            response.content,
            {"error": "Forbidden."}
        )
