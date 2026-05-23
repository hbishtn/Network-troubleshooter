from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tools/', views.tools, name='tools'),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("history/", views.history_view, name="history"),
    path("live-status/", views.live_status),
    path("more/", views.more, name="more"),
    path(
    "download-report/",
    views.download_report,
    name="download_report"
),
]