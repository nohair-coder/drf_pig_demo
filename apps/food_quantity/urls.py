from django.urls import path, re_path
from ..food_quantity import views

urlpatterns = [
    # path('', views.hello),
    path('', views.SetIntake.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
