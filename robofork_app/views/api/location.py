from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import django.urls as urls
import json
from robofork_app.models.location import Location


@csrf_exempt
def map_config(request, location_id=-1):
    location_model = get_object_or_404(Location, pk=location_id)
    map_info = json.loads(location_model.map_information_json)

    # マップ情報編集
    map_info["config"]["imageUrl"] = urls.reverse('api_file', args=(location_id,))
    del map_info["config"]["imageFileId"]

    # TODO: 車両情報をマップConfigへ追加。それとVehicleにLocation関連がなかった...

    return JsonResponse(map_info)
