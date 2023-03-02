import typing as tp
from abc import ABC, abstractmethod

from todo_app.models import Task


class ITodoService(ABC):
    @abstractmethod
    def get_all(self) -> tp.Iterable[Task]:
        raise NotImplementedError()

    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_all_user_tasks(self) -> tp.Iterable[Task]:
        raise NotImplementedError()


class TodoService(ITodoService):
    def get_all(self):
        return Task.objects.all()

    def create(self, user, todo):
        Task.objects.create(user=user, **todo)
        return

    def get_all_user_tasks(self, user):
        tasks = Task.objects.filter(user=user)
        return tasks


def get_todo_service():
    return TodoService()
