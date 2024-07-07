from django.urls import path
from . import views

app_name = 'userauths' 


urlpatterns = [
    path('signin/', views.signIn, name='signin'),
    path('signup/', views.signUp, name='register'),
    path('signout/', views.signOut, name='signOut'),
    path('profile/', views.profile, name='profile'),
    path('billing/', views.update_billing_info, name='billing_info'),

]
