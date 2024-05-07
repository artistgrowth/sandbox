from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

# app_name = "api"
urlpatterns = [
    path("questions/", views.QuestionViewSet.as_view({'patch': 'multi_update', 'get' : 'list'}), name='multi-update'),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
