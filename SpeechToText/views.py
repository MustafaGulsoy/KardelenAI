import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .Utils.speech_to_text import test


@method_decorator(csrf_exempt, name='dispatch')
class VoiceAnalysis(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        # Extract the image data
        image_data_base64 = data.get('base64_voice_data')
        result = test(image_data_base64)

        return JsonResponse({"Result": result})
