from django.contrib.auth.models import Group, User

from rest_framework import serializers

from polls.models import Choice, Question


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ["url", "votes", "choice_text"]


class QuestionListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        # this only works for PATCH, for UPDATE we need to take in mind creations and deletions
        updates = []
        for instance_id, instance in enumerate(instances):
            updates.append(self.child.update(instance, self.validated_data[instance_id]))
        return updates


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True)

    class Meta:
        model = Question
        fields = ["url", "question_text", "pub_date", "choices", "date_created"]
        list_serializer_class = QuestionListSerializer
