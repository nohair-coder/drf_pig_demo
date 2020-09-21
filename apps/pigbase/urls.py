from django.urls import path, re_path
from ..pigbase import views

urlpatterns = [
    # path('', views.hello),
    path('', views.PigBaseCheck.as_view()),
    path('4G/', views.PigBase4G.as_view()),
    # re_path('(?P<year>\d+)/(?P<mouth>\w*)/$', views.helloWorld),
]
