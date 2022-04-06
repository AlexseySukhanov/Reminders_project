"""reminder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('auth/',views.authuser, name='authuser'),
    path('logout/',views.logoutuser, name='logoutuser'),
    path('login/',views.loginuser, name='loginuser'),
    #Todo
    path('current/',views.currentuser, name='currentuser'),
    path('create/',views.createtodo, name='createtodo'),
    path('reminder/<int:reminder_pk>',views.view_reminder, name='view_reminder'),
    path('reminder/<int:reminder_pk>/complete',views.complete_reminder, name='complete_reminder'),
    path('reminder/<int:reminder_pk>/delete',views.delete_reminder, name='delete_reminder'),
    path('completed/',views.completed_reminders, name='completed_reminders'),
    path('',views.home, name='home')
]
