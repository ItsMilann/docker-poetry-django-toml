from __future__ import annotations

import typing

from django.utils.translation import gettext_lazy as _

if typing.TYPE_CHECKING:
    from users.models import User


def get_or_create_user(data, **kwargs) -> tuple[User, dict]:
    # pylint: disable=import-outside-toplevel
    """Update or create new user based on data."""
    from users.models import User
    from users.serializers import UserSerializer

    data = data.get("data", data)
    email = data["email"]

    qs = User.objects.filter(email=email)
    if qs.exists():
        instance = qs.latest("id")
        serializer = UserSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
    else:
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**kwargs)
    instance.password = data["password"]
    instance.save()
    return instance, serializer.data
