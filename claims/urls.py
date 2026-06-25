from django.urls import path

from .views import ClaimCreateView, ClaimDeleteView, ClaimDetailView, ClaimListView, ClaimUpdateView


urlpatterns = [
    path('claims/', ClaimListView.as_view(), name='claim_list'),
    path('claims/create/', ClaimCreateView.as_view(), name='claim_create'),
    path('claims/<int:pk>/', ClaimDetailView.as_view(), name='claim_detail'),
    path('claims/<int:pk>/edit/', ClaimUpdateView.as_view(), name='claim_update'),
    path('claims/<int:pk>/delete/', ClaimDeleteView.as_view(), name='claim_delete'),
]
