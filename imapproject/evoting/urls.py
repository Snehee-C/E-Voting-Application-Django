from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupPage, name='signup'),
    path('register/', views.register, name='register'),
    path('votespage/<str:question_id>/vote/', views.vote, name='vote'),
    path('', views.HomePage, name='home'),
    path('homepage/', views.HomePage, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('result/', views.results, name='result'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('notice/', views.notice, name='notice'),
    path('voting/', views.votespage, name='votespage'),
    path('<int:question_id>/', views.detail, name='detail'),
]
