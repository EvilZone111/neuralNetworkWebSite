from django.urls import path
from .views import MainView, image_analysis_view

app_name = 'neuralNetwork'
urlpatterns = [
    path('', MainView.as_view(), name='main-view'),
    path('analysis/', image_analysis_view, name='analysis'),
]