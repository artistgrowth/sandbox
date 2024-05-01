from django.contrib.auth.models import User, Group
from rest_framework import permissions
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
    queryset = Question.objects.prefetch_related("choice_set").all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def bulk_update(self, request):
        id_to_question_text = {}
        for data in request.data:
            url_parts = data["url"].strip("/").split("/")
            question_id = int(url_parts[-1])
            id_to_question_text[question_id] = data["question_text"]

        instances = Question.objects.filter(id__in=id_to_question_text.keys())

        serializer = self.get_serializer(instances, data=request.data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)

        updates = []
        for question in instances:
            updates.append(serializer.child.update(question, {'question_text':id_to_question_text[question.id]}))

        Question.objects.bulk_update(updates, ["question_text"])

        return Response({"results": serializer.data})


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
