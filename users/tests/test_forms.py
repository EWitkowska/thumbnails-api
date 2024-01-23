from users.forms import UserAdminChangeForm, UserAdminCreationForm


class TestUserAdminChangeForm:
    def test_form_field_class(self, user):
        form = UserAdminChangeForm(instance=user)

        assert form.fields["email"].__class__.__name__ == "EmailField"


class TestUserAdminCreationForm:
    def test_username_validation_error_msg(self, user):
        form = UserAdminCreationForm(
            {
                "email": user.email,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
        assert form.errors["email"][0] == "This email has already been taken."
