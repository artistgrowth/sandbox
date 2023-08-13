import re

from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response

from polls.models import Question, Choice
from .serializers import UserSerializer, GroupSerializer, QuestionSerializer, ChoiceSerializer


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
    # Prefetch related is your friend.  It's a great way to reduce the number of queries.
    queryset = Question.objects.all().prefetch_related("choice_set")
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # If the request data is a list, then we're doing a bulk partial update
        if isinstance(request.data, list):
            return self.bulk_partial_update(request, *args, **kwargs)
        # Otherwise, we're doing a single partial update. Business as usual.
        return self.partial_update(request, *args, **kwargs)

    def bulk_partial_update(self, request, *args, **kwargs):
        updated_questions = []
        for question_data in request.data:
            # Extract the question ID from the URL
            question_id = int(question_data['url'].split("questions/")[1].split("/")[0])
            try:
                question = Question.objects.get(pk=question_id)

                serializer = self.get_serializer(question, data=question_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_questions.append(serializer.data)
            except Question.DoesNotExist:
                return Response({"detail": f"Question with ID {question_id} does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"results": updated_questions}, status=status.HTTP_200_OK)


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
