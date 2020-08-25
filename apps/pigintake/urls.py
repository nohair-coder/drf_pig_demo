from django.urls import path, re_path
from ..pigintake import views

urlpatterns = [
    # path('', views.hello),
    path('', views.IntakeData.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
