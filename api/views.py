from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, status
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
    queryset = Question.objects.all()
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
                obj = get_object_or_404(Question, pk=id)
                obj.question_text = data["question_text"]
                obj.save()
                # question = get_object_or_404(Question, pk=id)
                # question.update(question_text=data["question_text"])
                ids_updated.append((id, data["question_text"]))
            
            return Response(data={"results": ids_updated}, status=status.HTTP_200_OK)
        else:
            question = get_object_or_404(Question, pk=pk)
            serializer_context = {
                'request': request,
            }
            serializer = QuestionSerializer(instance=question, context=serializer_context)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
