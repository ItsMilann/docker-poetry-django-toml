from django.db.models import TextChoices


class Roles(TextChoices):
    SUPER_ADMIN = "SUPERADMIN", "SUPERADMIN"
    ADMIN = "ADMIN", "ADMIN"
    RESEARCHER = "RESEARCHER", "RESEARCHER"
    SECRETORY = "SECRETORY", "SECRETORY"
    MEMBER = "MEMBER", "MEMBER"
    CHAIRMAN = "CHAIRMAN", "CHAIRMAN"
