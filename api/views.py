from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.request import Request
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
    queryset = Question.objects.prefetch_related('choice_set').all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request: Request, pk=None):
        """
        Method to partial update the information of a question
        
        Parameters
        ----------
        request: rest_framework.request.Request
            Request received with the information to update
        
        pk: Int
            Primary key or id of the object to update
        
        Returns
        -------
        rest_framework.response.Response
            Response with the id, and the data that was updated
        """
        if isinstance(request.data, list):
            ids = [d["url"].split("/")[-2] for d in request.data]
            ids_updated = []
            for id, data in zip(ids, request.data):
                question = get_object_or_404(Question, pk=id)
                question.question_text = data["question_text"]
                question.save()
                ids_updated.append((id, data["question_text"]))
            return Response(data={"results": ids_updated}, status=status.HTTP_200_OK)
        else:
            question = get_object_or_404(Question, pk=pk)
            question.question_text = data["question_text"]
            question.save()
            return Response(data={"results": [(pk, data["question_text"])]}, status=status.HTTP_200_OK)

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
