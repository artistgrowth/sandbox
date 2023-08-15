from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response

from polls.models import Question, Choice
from .serializers import UserSerializer, GroupSerializer, QuestionSerializer, ChoiceSerializer

import pdb, time

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

    def patch(self, request, *args, **kwargs):
        payload = request.data
        instances = []
        question_objects = Question.objects.all()

        for data in payload:
            id = int(str(data['url']).split("/")[-2])
            question_object = Question.objects.get(id=id)
            question_object.question_text = data["question_text"]
            question_object.save()
            instances.append(question_object)
            # if self.serializer_class(Question, Question.objects.all(), many=True).is_valid():

        # You don't need to use the is_valid() method on the serializer
        # because you're not deserializing data. Instead, you're directly updating the objects.
        # if self.serializer_class(data=instances).is_valid():
        #     updates = Question.objects.bulk_update(objs=data['question_text'], fields=["question_text"])
        #     print(updates)

        return Response(dict(results=len(instances)), status=status.HTTP_200_OK)

        # objs = Question.objects.all().filter(id_inn=question_ids)
        # updates = Question.objects.bulk_update(objs=data['question_text'], fields=["question_text"])
        # pdb.set_trace()



class ChoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows polls to be viewed or edited.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
