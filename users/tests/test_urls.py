from django.urls import resolve, reverse


class TestUserUrls:
    def test_user_detail(self, user):
        assert (
            reverse("users-detail", kwargs={"pk": user.pk})
            == f"/api/v1/users/{user.pk}/"
        )
        assert resolve(f"/api/v1/users/{user.pk}/").view_name == "users-detail"

    def test_user_list(self):
        assert reverse("users-list") == "/api/v1/users/"
        assert resolve("/api/v1/users/").view_name == "users-list"
