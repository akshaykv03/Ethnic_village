"""
URL configuration for ethnic project.

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
from ethnicapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,),
    path('reg',views.reg),
    path('login',views.login),

    path('adminHome',views.adminHome),
    path('adminUser',views.adminUser),
    path('adminActiveUser',views.adminActiveUser),
    path('adminManager',views.adminManager),
    path('adminActiveManager',views.adminActiveManager),
    path('adminProperties',views.adminProperties),
    path('adminBookings',views.adminBookings),
    path('adminFeedbacks',views.adminFeedbacks),

    path('userHome',views.userHome),
    path('userProperties',views.userProperties),
    path('userBook',views.userBook),
    path('userPay',views.userPay),
    path('userBookings',views.userBookings),
    path('userRequests',views.userRequests),
    path('userFeedback',views.userFeedback),

    path('manHome',views.manHome),
    path('manProperties',views.manProperties),
    path('propertyAvailable',views.propertyAvailable),
    path('manAddAmount',views.manAddAmount),
    path('manBookings',views.manBookings),
    path('manBookComplete',views.manBookComplete),
    path('manApprove',views.manApprove),
    path('manComplete',views.manComplete),
    path('manFeedbacks',views.manFeedbacks),
]
