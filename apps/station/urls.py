from django.urls import path, re_path
from ..station import views

urlpatterns = [
    # path('', views.hello),
    path('', views.StationCheck.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
