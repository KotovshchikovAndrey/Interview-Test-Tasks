from rest_framework import mixins, viewsets
from rest_framework.response import Response

from auth_app.middlewares.auth_backend import JWTAuthenticationBackend
from todo_app.permissions import IsTaskOwnerPermission
from todo_app.serializers import TodoSerializer
from todo_app.services.todo import get_todo_service


class TodoViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsTaskOwnerPermission,)
    authentication_classes = (JWTAuthenticationBackend,)

    serializer_class = TodoSerializer
    service = get_todo_service()

    def list(self, request):
        tasks = self.service.get_all_user_tasks(request.user)
        serializer = self.get_serializer(tasks, many=True)

        return Response(status=200, data=serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        self.service.create(user=request.user, todo=serializer.data)
        return Response(status=201)

    def get_queryset(self):
        return self.service.get_all()
