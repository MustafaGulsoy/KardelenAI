import os

import requests
from django.http import JsonResponse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL of the external API

        api_url = os.getenv('AUTH_IP', 'fallback-ip') + ':30028/gateway/auth/api/v1/Session/isActive'
        # api_url = 'https://pacs.konyasm.gov.tr:30028/gateway/auth/api/v1/Session/isActive'
        # 'https://pacs.konyasm.gov.tr:30028/gateway/auth/api/v1/Token'
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        # Headers for the API request (if needed)
        headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json',
        }

        try:
            # Send the GET request to the external API
            response = requests.get(api_url, headers=headers)

            if response.status_code != 200:
                return JsonResponse({
                    'error': 'Unauthorized attempt',
                    'status_code': response.status_code,
                    'reason': response.reason,
                    'text': response.text
                }, status=response.status_code)
        except requests.RequestException as e:
            # Handle any errors that occur during the request
            return JsonResponse({'error': str(e)}, status=500)

        return self.get_response(request)
