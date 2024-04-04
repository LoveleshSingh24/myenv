from django.urls import path 
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('leaderboard',views.leaderboard_view,name='leaderboard'),
    path('dashboard',views.dashboard_view,name='dashboard'),

]
