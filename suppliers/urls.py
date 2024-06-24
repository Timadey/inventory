"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from suppliers.views import (SupplierItemListCreateView, 
                             ListCreateSupplierView, 
                             RetrieveUpdateDestroySupplierView,
                             SupplierItemRemoveView,)


urlpatterns = [
    path('suppliers/', ListCreateSupplierView.as_view(), name='suppliers'),
    path('suppliers/<uuid:supplier>', RetrieveUpdateDestroySupplierView.as_view(), name='supplier'),
    path('suppliers/<uuid:supplier>/items', SupplierItemListCreateView.as_view(), name='supplier-item'),
    path('suppliers/<uuid:supplier>/remove-items', SupplierItemRemoveView.as_view(), name='supplier-remove-item'),

]
