from todo_app.models import RepositoryFactory


class TodoService:
    def __init__(self) -> None:
        self.repository = RepositoryFactory.get_repository("TodoRepository")

    def get_all(self):
        return self.repository.all()

    def create(self, user, todo):
        self.repository.create(user=user, **todo)
        return

    def get_all_user_tasks(self, user):
        tasks = self.repository.filter(user=user)
        return tasks
