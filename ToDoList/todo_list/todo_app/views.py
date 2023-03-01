from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from auth_app.middlewares.auth_backend import JWTAuthenticationBackend
from todo_app.permissions import IsTaskOwnerPermission
from todo_app.serializers import TodoSerializer
from todo_app.services.factory import ServiceFactory


class TodoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsTaskOwnerPermission,)
    authentication_classes = (JWTAuthenticationBackend,)

    serializer_class = TodoSerializer
    service = ServiceFactory.get_service("TodoService")

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        self.service.create(user=request.user, todo=serializer.data)
        return Response(status=201)

    @action(detail=False, methods=["get"])
    def user_tasks(self, request):
        tasks = self.service.get_all_user_tasks(request.user)
        serializer = self.get_serializer(tasks, many=True)

        return Response(status=200, data=serializer.data)

    def get_queryset(self):
        return self.service.get_all()
