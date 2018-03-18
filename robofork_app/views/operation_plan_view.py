from django.views.generic import ListView, TemplateView
from ._base_view import BaseTemplateViewMixIn
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan


class OperationPlanIndexView(BaseTemplateViewMixIn, ListView):
    template_name = "robofork_app/operation_plan/index.html"
    model = VehicleOperationPlan


class OperationPlanDetailView(BaseTemplateViewMixIn, TemplateView):
    template_name = "robofork_app/operation_plan/detail.html"
