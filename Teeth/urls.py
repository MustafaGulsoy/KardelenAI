
from django.urls import path

from Teeth.views import ToothXrayAnalysisView
    # ToothXRayProcessor)

urlpatterns = [
    path('tooth-x-ray-analysis', ToothXrayAnalysisView.as_view(), name='analyze_tooth_xray'),

]
