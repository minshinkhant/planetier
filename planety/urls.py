from django.urls import path
from . import views

app_name = 'planety'

urlpatterns = [
    path('', views.ListPlanety.as_view(), name='all'),
    path('new/', views.CreatePlanety.as_view(), name='create'),
    path('broadcasts/in/<slug:slug>',
         views.SinglePlanety.as_view(), name='single'),
    path('join/<slug:slug>', views.JoinPlanety.as_view(), name='join'),
    path('leave/<slug:slug>', views.LeavePlanety.as_view(), name='leave'),
]
