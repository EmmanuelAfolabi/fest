from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('connect-crews', views.connectcrews, name='connect-crews'),
    path('connect-users', views.connectusers, name='connect-users'),
    path('dashboard-crew', views.dashboardcrew, name='dashboard-crew'),
    #path('dashboard-user/<str:id>/', views.dashboarduser, name='dashboard-user'),
    path('dashboard-user', views.dashboarduser, name='dashboard-user'),

]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
