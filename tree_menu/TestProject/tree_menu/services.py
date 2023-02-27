import typing as tp
from django.db.models import Model
from tree_menu import models

Menu = tp.TypeVar("Menu", bound=Model)
MenuItem = tp.TypeVar("MenuItem", bound=Model)


class MenuService(tp.Generic[Menu, MenuItem]):
    menu: tp.Type[Menu]
    menu_item: tp.Type[MenuItem]

    def __init__(
        self,
        menu: tp.Type[Menu],
        menu_item: tp.Type[MenuItem],
    ) -> None:
        self.menu = menu
        self.menu_item = menu_item

    def get_menu_items(self, menu_name: str):
        menu = self.menu_item.objects.filter(menu__name=menu_name, parent=None)
        return menu

    def get_item_parents_count(self, item_id: int):
        item = self.menu_item.objects.filter(id=item_id).first()
        if item is None:
            return

        item_parents_count = 0
        current_parent = item.parent
        while current_parent is not None:
            item_parents_count += 1
            current_parent = current_parent.parent

        return item_parents_count

    def draw_tree_menu(
        self,
        menu_items: tp.List[MenuItem],
        limit: int = 1,
        tree="",
    ):
        for menu_item in menu_items:
            if limit == 0:
                break

            tree += f"""
            <li>
                <a href="">{menu_item.name}</a>
            </li>
            """

            item_children = menu_item.children.all()
            if item_children:
                childen_tree = self.draw_tree_menu(
                    menu_items=item_children, limit=limit - 1
                )
                tree += f"<ul>{childen_tree}</ul"

        return tree


class ServiceFactory:
    services = {
        "menu": MenuService(models.Menu, models.MenuItem),
    }

    @classmethod
    def create(cls, name: str):
        return cls.services.get(name)
