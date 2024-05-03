from django.contrib.auth.models import Group, User

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from polls.models import Choice, Question

from .serializers import ChoiceSerializer, GroupSerializer, QuestionSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """

    queryset = Question.objects.prefetch_related("choice_set").all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    additional_routes_by_method = {
        "patch": "partial_update_many",
    }

    def partial_update_many(self, request, *args, **kwargs):
        partial = True
        ids = [r["url"].strip("/").split("/")[-1] for r in request.data]
        # if we only allow to update root attributes, not child (like choices), this is good
        # if not we need to delete instance._prefetched_objects_cache to prevent cache
        instances = Question.objects.prefetch_related("choice_set").filter(id__in=ids)
        serializer = self.get_serializer(instances, data=request.data, many=True, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update_many(serializer)
        return Response({"results": serializer.data})

    def perform_update_many(self, serializer):
        return serializer.save()


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
