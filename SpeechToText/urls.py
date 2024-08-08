from django.urls import path

from SpeechToText.views import VoiceAnalysis

urlpatterns = [
    # path('voice-analysis', SpeechToTextUtil.transcribe_audio(), name='VoiceAnalysis'),
    path('voice-analysis',  VoiceAnalysis.as_view(), name='VoiceAnalysis'),

    # path('test', VoiceAnalysis.test(), name='test'),

]
