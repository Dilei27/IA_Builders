from django.urls import path

from .views import (
    CommissionCreateView,
    CommissionDeleteView,
    CommissionDetailView,
    CommissionListView,
    CommissionUpdateView,
    RepasseListView,
)


urlpatterns = [
    path('commissions/', CommissionListView.as_view(), name='commission_list'),
    path('commissions/create/', CommissionCreateView.as_view(), name='commission_create'),
    path('commissions/<int:pk>/', CommissionDetailView.as_view(), name='commission_detail'),
    path('commissions/<int:pk>/edit/', CommissionUpdateView.as_view(), name='commission_update'),
    path('commissions/<int:pk>/delete/', CommissionDeleteView.as_view(), name='commission_delete'),
    path('repasses/', RepasseListView.as_view(), name='repasse_list'),
]
