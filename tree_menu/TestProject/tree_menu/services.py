import typing as tp
from django.db.models import Model
from tree_menu import models

Menu = tp.TypeVar("Menu", bound=Model)
MenuItem = tp.TypeVar("MenuItem", bound=Model)


class MenuService(tp.Generic[Menu, MenuItem]):
    menu: tp.Type[Menu]
    menu_item: tp.Type[MenuItem]

    def __init__(self, menu: tp.Type[Menu], menu_item: tp.Type[MenuItem]) -> None:
        self.menu = menu
        self.menu_item = menu_item

    def get_menu_items(self, menu_name: str):
        menu_items = self.menu_item.objects.filter(
            menu__name=menu_name,
            parent=None,
        ).values()

        return menu_items

    def get_tree_menu(self, menu_name: str):
        items = self.menu_item.objects.filter(
            menu__name=menu_name,
            parent=None,
        ).values()

        for item in items:
            item["children"] = self.get_item_children(item_id=item["id"])

        return items

    def get_item_children(self, item_id: int):
        children = self.menu_item.objects.filter(parent=item_id).values("id", "name")
        for child in children:
            child["children"] = self.get_item_children(child["id"])

        return children

    def get_item_parents_id(self, item_id: int):
        item = self.menu_item.objects.filter(id=item_id).first()

        parent = item.parent
        parents_id = []
        while parent is not None:
            parents_id.append(parent.id)
            parent = parent.parent

        return parents_id


class ServiceFactory:
    services = {
        "menu": MenuService(models.Menu, models.MenuItem),
    }

    @classmethod
    def create(cls, name: str):
        return cls.services.get(name)
