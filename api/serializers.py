from rest_framework import serializers
from .models import Analyzer, CHOICES


class WordSerializer(serializers.ModelSerializer):

    """ Сериализатор с переопределенным полем, для реализации множественного выбора. """

    method = serializers.MultipleChoiceField(choices=CHOICES)

    class Meta:
        model = Analyzer
        fields = ("method", "text")
        extra_kwargs = {'text': {'min_length': 20}}
