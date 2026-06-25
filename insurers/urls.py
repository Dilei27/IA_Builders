from django.urls import path

from .views import (
    BranchCreateView,
    BranchDeleteView,
    BranchDetailView,
    BranchListView,
    BranchUpdateView,
    CoverageCreateView,
    CoverageDeleteView,
    CoverageDetailView,
    CoverageListView,
    CoverageUpdateView,
    InsurerCreateView,
    InsurerDeleteView,
    InsurerDetailView,
    InsurerListView,
    InsurerUpdateView,
)


urlpatterns = [
    path('insurers/', InsurerListView.as_view(), name='insurer_list'),
    path('insurers/create/', InsurerCreateView.as_view(), name='insurer_create'),
    path('insurers/<int:pk>/', InsurerDetailView.as_view(), name='insurer_detail'),
    path('insurers/<int:pk>/edit/', InsurerUpdateView.as_view(), name='insurer_update'),
    path('insurers/<int:pk>/delete/', InsurerDeleteView.as_view(), name='insurer_delete'),
    path('branches/', BranchListView.as_view(), name='branch_list'),
    path('branches/create/', BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch_detail'),
    path('branches/<int:pk>/edit/', BranchUpdateView.as_view(), name='branch_update'),
    path('branches/<int:pk>/delete/', BranchDeleteView.as_view(), name='branch_delete'),
    path('coverages/', CoverageListView.as_view(), name='coverage_list'),
    path('coverages/create/', CoverageCreateView.as_view(), name='coverage_create'),
    path('coverages/<int:pk>/', CoverageDetailView.as_view(), name='coverage_detail'),
    path('coverages/<int:pk>/edit/', CoverageUpdateView.as_view(), name='coverage_update'),
    path('coverages/<int:pk>/delete/', CoverageDeleteView.as_view(), name='coverage_delete'),
]
