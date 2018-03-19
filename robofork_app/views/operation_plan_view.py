from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect
import django.urls as urls
from ._base_view import BaseViewMixIn
from robofork_app.models.vehicle_operation_plan import VehicleOperationPlan

"""
Class Based View と Function Based View が混在してキモいけど、
django学習中なのでどっちがいいか分からない。しばらくは混在させていく。
ListViewはPagination自動でやってくれるみたいで、ちょっと使ってみたいんだ。
"""


class OperationPlanIndexView(BaseViewMixIn, ListView):
    template_name = "robofork_app/operation_plan/index.html"
    model = VehicleOperationPlan


class OperationPlanDetailView(BaseViewMixIn, TemplateView):
    template_name = "robofork_app/operation_plan/detail.html"


def detail_new(request, location_id):
    # このページはSPAでAjaxで動いてる。新規作成でも仮にIDを採番しないとエラーになるのでこうしてる
    next_id = VehicleOperationPlan.next_id()
    return redirect(urls.reverse('operation_plan_detail', kwargs={
        "location_id": location_id,
        "vehicle_operation_plan_id": next_id,
    }))
