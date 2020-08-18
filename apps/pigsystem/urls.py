from django.urls import path, re_path
from .views import SystemCheck

urlpatterns = [
    # path('', views.hello),
    path('', SystemCheck.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
