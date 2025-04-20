from django.contrib import admin
from django.urls import path, include
from predictor import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')),
    path('login/', LoginView.as_view(template_name='predictor/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='predict_price'), name='logout'),
    path('how-the-model-works/', views.how_the_model_works, name='model_works'),
    path('interpret-predictions/', views.interpret_predictions, name='pred_interpretation'),
    path('faqs/', views.faqs, name='faqs'),
]