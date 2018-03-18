from django.views.generic import TemplateView


class OperationPlanIndexView(TemplateView):
    template_name = "robofork_app/operation_plan/index.html"


class OperationPlanDetailView(TemplateView):
    template_name = "robofork_app/operation_plan/detail.html"
