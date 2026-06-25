from django.urls import path

from .views import RenewalCreateView, RenewalDeleteView, RenewalDetailView, RenewalListView, RenewalUpdateView


urlpatterns = [
    path('renewals/', RenewalListView.as_view(), name='renewal_list'),
    path('renewals/create/', RenewalCreateView.as_view(), name='renewal_create'),
    path('renewals/<int:pk>/', RenewalDetailView.as_view(), name='renewal_detail'),
    path('renewals/<int:pk>/edit/', RenewalUpdateView.as_view(), name='renewal_update'),
    path('renewals/<int:pk>/delete/', RenewalDeleteView.as_view(), name='renewal_delete'),
]
