from django.urls import path
from . import views

urlpatterns = [
    path('access/', views.access, name='access'),
    path('loc/', views.loc, name='loc'),
    path('unloc/', views.unloc, name='unloc'),
]
