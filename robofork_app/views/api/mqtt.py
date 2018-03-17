from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from robofork_app.libs import mqtt


@csrf_exempt
def send(request):
    # QoS設定
    qos = int(request.POST.get('qos', mqtt.MQTT_QOS_GOOD))

    # MQTT送信
    ret = mqtt.send("1", request.POST['can_id'], request.POST['can_data'], qos=qos)
    return JsonResponse({'result': ret})
