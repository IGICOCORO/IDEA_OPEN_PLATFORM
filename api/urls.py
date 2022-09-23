from django.urls import path, include

from rest_framework import routers
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

from .views import *

schema_view = get_swagger_view(title='Pastebin API')

router = routers.DefaultRouter()

router.register("Tags", TagsViewset)
router.register("Post", PostViewset)
router.register("Comments", CommentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('doc/', schema_view),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
