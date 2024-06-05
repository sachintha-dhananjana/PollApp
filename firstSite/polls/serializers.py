from django.utils import timezone
from rest_framework import serializers

from .models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ('question',)


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,read_only=True)

    class Meta:
        model = Question
        fields =  ['question_text', 'pub_date', 'choices']
        depth = 1

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        if 'pub_date' not in validated_data:
            validated_data['pub_date'] = timezone.now()
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question
