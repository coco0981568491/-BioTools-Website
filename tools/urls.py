from django.urls import path
from .views import home, findNPosPage, aLPCutterPage

urlpatterns = [
    path('', home),
    path('findNPos/', findNPosPage),
    path('aLPCutter/', aLPCutterPage),
]
