from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterView,LoginView,QuestionsView, ResponseView, BulkResponseView, logoutView, RequestPasswordReset,ResetPassword
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# router = DefaultRouter()
# router.register(r'response', ResponseView,basename='response')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutView.as_view(), name='logout'),
     path('password_reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password_reset/confirm/<token>/', ResetPassword.as_view(), name='password'),
    path('questions/', QuestionsView.as_view(), name='questions'),
    path('response/', ResponseView.as_view(), name='response'),
    path('bulkresponse/', BulkResponseView.as_view(), name =" bulkresponse"),
    path('disordersrecommendations/', views.Disorder_recommendation, name='disorders'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('', include(router.urls)), 
]

