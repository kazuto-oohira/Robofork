from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "robofork_app/login.html"
