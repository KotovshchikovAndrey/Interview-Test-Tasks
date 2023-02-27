from django import template
from tree_menu.services import ServiceFactory

register = template.Library()


@register.simple_tag(name="draw_menu", takes_context=True)
def get_menu(context, name: str):
    request = context["request"]

    service = ServiceFactory.create("menu")
    menu_items = service.get_menu_items(name)

    current_item_id = request.GET.get("item_id")
    if current_item_id is None:
        tree = service.draw_tree_menu(menu_items=menu_items)
        return template.Template(tree).render(context)

    item_parents_count = service.get_item_parents_count(item_id=current_item_id)
    tree = service.draw_tree_menu(
        menu_items=menu_items,
        limit=item_parents_count + 1,
    )

    return template.Template(tree).render(context)
