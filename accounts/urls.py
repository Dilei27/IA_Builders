from django.urls import path

from .views import LandingView, SignupView


urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
]
