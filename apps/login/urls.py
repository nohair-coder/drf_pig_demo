from django.urls import path, re_path
from ..login import views

urlpatterns = [
    # path('', views.hello),
    path('', views.LoginCheck.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
