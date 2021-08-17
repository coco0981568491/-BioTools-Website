from django.urls import path
from .views import home, findNPosPage, aLPCutterPage, findOPosPage

urlpatterns = [
    path('', home),
    path('findNPos/', findNPosPage),
    path('findOPos/', findOPosPage),
    path('aLPCutter/', aLPCutterPage),
]
