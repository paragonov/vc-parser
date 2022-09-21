from django.urls import path

from .views import VcMVListView, VcDNSListView, VcCLListView

urlpatterns = [
    path('mvideo/', VcMVListView.as_view(), name='mvideo'),
    path('dns/', VcDNSListView.as_view(), name='dns'),
    path('citilink/', VcCLListView.as_view(), name='citilink')
]
