from django.apps import apps as django_apps

from rest_framework import serializers

from rest_framework_jwt.settings import api_settings


class Serializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(*args, **kwargs)


def get_user_model():
    """
    Returns the User model will be used for JWT authentication.
    """
    try:
        return django_apps.get_model(api_settings.JWT_AUTH_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("JWT_AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "JWT_AUTH_USER_MODEL refers to model '%s' that has not been installed" % api_settings.JWT_AUTH_USER_MODEL
        )


def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
    except:
        username_field = 'username'

    return username_field


def get_username(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return username
