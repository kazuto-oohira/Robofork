from django.views.generic import TemplateView


class OperationPlanDetailView(TemplateView):
    template_name = "robofork_app/operation_plan/detail/index.html"
