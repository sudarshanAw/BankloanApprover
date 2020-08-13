from django.urls import path
from loanform.views import customer_form

urlpatterns = [
    path('',customer_form, name = 'customer_form' ),

]
