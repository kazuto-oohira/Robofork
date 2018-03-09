from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from robofork_app.libs import mqtt


@csrf_exempt
def send(request):
    # MQTT送信
    ret = mqtt.send("1", request.POST['can_id'], request.POST['can_data'])
    return JsonResponse({'result': ret})
