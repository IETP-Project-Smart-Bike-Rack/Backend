from django.urls import path
from . import views

urlpatterns = [
    path('login_page/',views.access_get,name='login_page'),
    path('access_post/', views.access_post, name='access'),
    path('scan/',views.lock_rack_page, name='lock rack'),
    path('loc/', views.loc, name='lock'),
    path('unlockpage/',views.unlock_page, name='unlock page'),
    path('unloc/', views.unloc, name='unlock'),
    path('unlocked-racks_get_unlocked_racks/', views.get_unlocked_racks, name='get_unlocked_racks'),
    path('locked-racks_get_locked_racks/', views.get_locked_racks, name='get_locked_racks'),
    path('get_user_id/', views.get_user_id, name='get_user_id'),
]
