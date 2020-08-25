from django.urls import path, re_path
from ..pigsystem import views

urlpatterns = [
    # path('', views.hello),
    path('', views.SystemCheck.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
