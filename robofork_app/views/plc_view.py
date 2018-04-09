from django.http import JsonResponse


def execute(request, plc_id):
    return JsonResponse({"result": True, "id": plc_id})
