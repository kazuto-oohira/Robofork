from django.views.generic import TemplateView


class VehicleControlView(TemplateView):
    template_name = "robofork_app/vehicle_control/index.html"
