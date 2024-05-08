"""Test User Login functionality."""

import pytest

from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from ..utilities import create_permission
from ..models import User
from ..views import admin_account

pytestmark = [pytest.mark.django_db]


class TestUserPermissions:
    """Test Permissions of users."""

    USER_MODEL = get_user_model()
    LOGIN_URL = reverse("account_login")

    @pytest.fixture
    def admin_user(self) -> User:
        """Create an Admin User (superuser)."""
        return self.USER_MODEL.objects.create_superuser(
            "admin", "admin@myproject.com", "password"
        )

    @pytest.fixture
    def user(self) -> User:
        """Create a User."""
        return self.USER_MODEL.objects.create_user(
            "user", "user@djforge.com", "pass123"
        )

    @pytest.fixture
    def user_content_type(self) -> ContentType:
        """Create Content Type Object."""
        return ContentType.objects.get_for_model(User)

    @pytest.fixture
    def admin_view_permission(self, user_content_type: ContentType) -> Permission:
        """Create Admin view Permission Object."""
        return create_permission(
            codename="can_view_admin_account",
            name="Can view Admin account",
            content_type=user_content_type,
        )

    @pytest.fixture
    def user_view_permission(self, user_content_type: ContentType) -> Permission:
        """Create User view Permission Object."""
        return create_permission(
            codename="can_view_user_account",
            name="Can view User account",
            content_type=user_content_type,
        )

    @pytest.fixture
    def admin_group(self, admin_view_permission: Permission):
        """Create Admin Group."""
        admin_group, _ = Group.objects.get_or_create(name="admin_group")
        admin_group.permissions.add(admin_view_permission)
        return admin_group

    @pytest.fixture
    def user_group(self, user_view_permission: Permission):
        """Create User Group."""
        user_group, _ = Group.objects.get_or_create(name="user_group")
        user_group.permissions.add(user_view_permission)
        return user_group

    def test_admin_group_has_admin_permission(
        self, admin_group: Group, admin_view_permission: Permission
    ):
        """Test if the Admin Group has the Admin View Permission."""
        assert admin_view_permission in admin_group.permissions.all()

    def test_user_group_has_user_permission(
        self, user_group: Group, user_view_permission: Permission
    ):
        """Test if the User Group has the User View Permission."""
        assert user_view_permission in user_group.permissions.all()

    def test_admin_in_admin_group(self, admin_group: Group, admin_user: User):
        """Test if Admin is assigned to the Admin Group."""
        admin_user.groups.add(admin_group)
        assert admin_user.groups.filter(name="admin_group").exists()

    def test_user_in_user_group(self, user_group: Group, user: User):
        """Test if User is assigned to the User Group."""
        user.groups.add(user_group)
        assert user.groups.filter(name="user_group").exists()

    def test_admin_account_page(self, admin_user):
        """Test the response of admin account page."""
        request = RequestFactory().get(reverse("dj_users/users/admin_account"))
        request.user = admin_user
        response = admin_account(request)
        assert response.status_code == 200
