from django.contrib.auth.models import User, Group
from rest_framework.decorators import action
from rest_framework import permissions, viewsets, mixins, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from polls.models import Question, Choice
from .serializers import UserSerializer, GroupSerializer, QuestionSerializer, ChoiceSerializer
from django.utils import timezone


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

    @action(detail=False, methods=['patch'])
    def bulk_update(self, request):
        """
        Custom action to handle bulk updates via PATCH method.
        """
        payload = request.data
        updated_objects = []

        for item in payload:
            id = item.get('id')  # Assuming 'id' key is present in each payload item
            question_instance = get_object_or_404(Question, id=id)
            serializer = self.get_serializer(question_instance, data=item, partial=True,  context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            updated_objects.append(serializer.data)
        
        return Response({"results": updated_objects}, status=status.HTTP_200_OK)




class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
