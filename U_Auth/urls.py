from django.urls import path
from U_Auth.views import *

urlpatterns = [
    path('admin_login/', admin_login, name='admin_login'),
    path('admin/logout/', admin_logout, name='admin_logout'),
]
