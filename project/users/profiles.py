from rest_framework.decorators import action
from users import models, serializers
from users.response import CustomModelViewSet as ModelViewSet


class ProfileViewSet(ModelViewSet):
    """
    Viewset for managing profiles.
    This viewset handles the CRUD operations for the `Profile` model.
    It provides endpoints for retrieving and updating profile information.
    """

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = []

    def get_queryset(self):
        role = self.request.query_params.get("role")
        qs = super().get_queryset()
        if role:
            qs = qs.filter(user__role=role)
        return qs

    @action(["POST", "GET"], detail=False)
    def info(self, request, *args, **kwargs):
        instance, _ = models.Profile.objects.get_or_create(user=request.user)
        self.get_object = lambda: instance
        if request.method == "GET":
            self.serializer_class = serializers.ProfileDetailSerializer
            return super().retrieve(request)
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class DocumentViewSet(ModelViewSet):
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    permission_classes = []

    def get_queryset(self):
        profile = self.request.query_params.get("profile")
        qs =  super().get_queryset()
        if profile:
            qs = qs.filter(profile=profile)
        return qs


class PaymentInfoViewSet(ModelViewSet):
    serializer_class = serializers.PaymentInfoSerializer
    queryset = models.PaymentInfo.objects.all()
    permission_classes = []

    def get_queryset(self):
        profile = self.request.query_params.get("profile")
        qs = super().get_queryset()
        if profile:
            qs = qs.filter(profile=profile)
        return qs

