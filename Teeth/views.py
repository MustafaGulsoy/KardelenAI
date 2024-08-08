import json

import numpy as np
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .Utils.process_tooth_x_ray import ToothXRayUtil, \
    process_xray  # Assuming you have a process_xray function in predict.py

processor = ToothXRayUtil()


class NumpyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return super().default(obj)


@method_decorator(csrf_exempt, name='dispatch')
class ToothXrayAnalysisView(View):
    async def post(self, request, *args, **kwargs):
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract the image data
            image_url = data.get('image_url')

            if not image_url:
                return JsonResponse({'error': 'No image data provided'}, status=400)
            authorization_header = request.META.get('HTTP_AUTHORIZATION').split(" ")[-1]
            # Headers for the API request (if needed)
            headers = {
                'Authorization': authorization_header,
            }

            processed_image, paired_results = await process_xray(image_url,header=headers)
            response = {
                'image_base64': processed_image,
                'result': paired_results
            }

            return JsonResponse(response, encoder=NumpyEncoder)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
