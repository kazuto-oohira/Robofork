import mimetypes, base64
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from robofork_app.models.file import File


@csrf_exempt
def file(request, file_id=-1):
    file_model = get_object_or_404(File, pk=file_id)
    print(file_model.type)
    return HttpResponse(content=base64.b64decode(file_model.data), content_type=file_model.type)

