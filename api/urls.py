from django.urls import path, include

from rest_framework import routers
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

from .views import *

router = routers.DefaultRouter()

router.register("Tags", TagsViewset)
router.register("Post", PostViewset)
router.register("Comments", CommentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
