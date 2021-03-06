from django.views.generic import TemplateView


class BaseViewMixIn(object):    # TemplateViewを親にすると多重継承でややこしいので...
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Location取得
        context['location_id'] = self.kwargs.get('location_id', 0)
        return context
