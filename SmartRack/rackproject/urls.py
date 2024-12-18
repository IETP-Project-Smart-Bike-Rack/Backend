from django.urls import path
from . import views

urlpatterns = [
    path('login_page/',views.access_get,name='login_page'),
    path('access/', views.access_post, name='access'),
    path('scan/',views.lock_rack_page, name='lock rack'),
    path('loc/', views.loc, name='lock'),
    path('unlockpage/',views.unlock_page, name='unlock page'),
    path('unloc/', views.unloc, name='unlock'),
]
