"""
URL configuration for project19 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from cherry.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
  
    path('insert_emp/',insert_emp,name='insert_emp'),
    path('display_data/',display_data,name='display_data'), 
    path('empdept/',empdept,name='empdept'),
    path('deptemp/',deptemp,name='deptemp'),
    path('aggregate_functions/',aggregate_functions,name='aggregate_functions'),
    path('update_data/',update_data,name='update_data'),
    path('deletion_data/',deletion_data,name='deletion_data'),
]
