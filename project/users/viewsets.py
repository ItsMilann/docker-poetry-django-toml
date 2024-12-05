# pylint:disable=W0201
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from users import models, serializers
from users.response import CustomModelViewSet as ModelVS
from users.response import CustomResponse as Response


class UserViewSet(ModelVS):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "me":
            return serializers.UserWithConfigSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ["update_password", "me"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(["get"], detail=False, url_path="update-password")
    def update_password(self, request, *args, **kwargs):
        password = request.data["password"]
        user = request.user
        user.set_password(password)
        user.save()
        self.get_object = lambda: user
        return self.retrieve(request, *args, **kwargs)

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):  # pylint:disable=invalid-name
        self.get_object = lambda: request.user
        return self.retrieve(request, *args, **kwargs)


class ObtainTokenView(TokenObtainPairView):
    serializer_class = serializers.TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=201)
