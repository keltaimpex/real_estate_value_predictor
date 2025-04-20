from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.predict_price, name='predict_price'),

    path('my_predictions/', views.my_predictions, name='my_predictions'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='predictor/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('prediction/<int:prediction_id>/', views.prediction_detail, name='prediction_detail'),
    path('how-the-model-works/', views.how_the_model_works, name='model_works'),
    path('interpret-predictions/', views.interpret_predictions, name='pred_interpretation'),
    path('faqs/', views.faqs, name='faqs'),


]