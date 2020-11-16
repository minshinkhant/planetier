from django.urls import path
from . import views

app_name = 'broadcasts'
urlpatterns = [
    path('', views.BroadcastList.as_view(), name='all'),
    path('new/', views.CreateBroadcast.as_view(), name='create'),
    path('by/<str:username>/', views.UserBroadcasts.as_view(), name='for_user'),
    path('by/<str:username>/<int:pk>/',
         views.BroadcastDetail.as_view(), name='single'),
    path('delete/<int:pk>/', views.DeleteBroadcast.as_view(), name='delete'),
]
