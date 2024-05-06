from django.urls import include, path
from rest_framework import routers
from . import custom_router
from . import views

router = custom_router.PatchRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

# app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework"))
]
