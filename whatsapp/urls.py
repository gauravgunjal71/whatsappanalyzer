from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('fileupload', views.fileupload),
    path('messagecount', views.messagecount),
    path('mostusedwords', views.mostusedwords)
]