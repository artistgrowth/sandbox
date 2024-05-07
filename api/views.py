from django.contrib.auth.models import User, Group
from django.urls import resolve
from django.urls.exceptions import Resolver404
from rest_framework import permissions
from rest_framework import status
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
    queryset = Question.objects.prefetch_related('choice_set').all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def multi_update(self, request, *args, **kwargs):
        if request.data and type(request.data) == list:        
            updates = request.data
            updated_questions = []
            for update in updates:
                url = update.get('url')
                question_text = update.get('question_text')
                try:
                    match = resolve(url)
                    question = Question.objects.get(id=match.kwargs.get('pk'))
                    question.question_text = question_text
                    question.save(update_fields=['question_text'])
                    updated_questions.append(question)
                except Resolver404:
                    print('invalid url: {}'.format(url))
                    continue
            serializer = QuestionSerializer(updated_questions, context={'request': request},many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
