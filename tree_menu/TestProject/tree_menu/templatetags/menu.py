from django import template
from tree_menu.services import ServiceFactory

register = template.Library()


@register.inclusion_tag("menu.html", name="draw_menu", takes_context=True)
def get_menu(context, name: str):
    context_data = {}
    service = ServiceFactory.create("menu")

    selected_item_id = context.get("item_id", None)
    if selected_item_id is None:
        context_data["menu_items"] = service.get_menu_items(menu_name=name)
        return context_data

    tree_menu = service.get_tree_menu(menu_name=name)
    item_parents_id = service.get_item_parents_id(item_id=selected_item_id)

    context_data["menu_items"] = tree_menu
    context_data["selected_item_id"] = selected_item_id
    context_data["selected_item_parents_id"] = item_parents_id

    return context_data
