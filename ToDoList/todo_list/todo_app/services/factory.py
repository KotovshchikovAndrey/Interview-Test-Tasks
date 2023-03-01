from todo_app.services.todo import TodoService


class ServiceFactory:
    services = {"TodoService": TodoService()}

    @classmethod
    def get_service(cls, name):
        return cls.services.get(name)
