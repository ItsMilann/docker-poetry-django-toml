from django.apps import AppConfig


class UserConfig(AppConfig):
    name = "users"

    def ready(self) -> None:
        # pylint:disable=import-outside-toplevel unused-import
        from users import signals
