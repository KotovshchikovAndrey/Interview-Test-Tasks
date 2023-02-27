from django.views import generic
from tree_menu.services import ServiceFactory


class MainPageView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
