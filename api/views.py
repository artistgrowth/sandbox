from django.contrib.auth.models import User, Group
from django.urls import resolve

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

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

    # Add .order_by() to ensure pagination yields consistent results
    queryset = Question.objects.all().prefetch_related('choice_set').order_by('-date_created')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['PATCH'], detail=False, url_path='bulk-update')
    def bulk_update(self, request):
        def add_serializer(instance_data):
            obj_id = resolve(instance_data.get('url')).kwargs['pk']
            question_obj = self.get_queryset().get(pk=obj_id)
            serializer = self.get_serializer(question_obj, data=instance_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return serializer
        response_data = None
        try:
            if isinstance(request.data, list):
                serializers = [add_serializer(instance) for instance in request.data]
                response_data = [x.data for x in serializers]
            else:
                response_data = add_serializer(request.data).data
            return Response(response_data, status=200)
        except Exception as e:
            print(e)
            raise ValidationError('Malformed request')


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
