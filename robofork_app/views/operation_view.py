from django.views.generic import TemplateView


class OperationIndexView(TemplateView):
    template_name = "robofork_app/operation_view/index.html"
