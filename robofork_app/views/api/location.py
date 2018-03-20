from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import django.urls as urls
import json

from robofork_app.models import Vehicle
from robofork_app.models.location import Location


@csrf_exempt
def map_config(request, location_id):
    location_model = get_object_or_404(Location, pk=location_id)
    map_info = json.loads(location_model.map_information_json)

    # マップ情報編集
    map_info["config"]["imageUrl"] = urls.reverse('api_file', args=(location_id,))
    del map_info["config"]["imageFileId"]

    # 場所に所属する車両
    vehicles = Vehicle.get_list(location_id=location_id)
    map_info["vehicles"] = []
    for vehicle in vehicles:
        map_info["vehicles"].append(vehicle.as_json())

    return JsonResponse(map_info)
