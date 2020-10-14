from rest_framework import serializers
from .models import Analyzer, User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "email", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("email", )


class WordSerializer(serializers.ModelSerializer):

    """ Сериализатор с переопределенным полем, для реализации множественного выбора. """

    method = serializers.MultipleChoiceField(choices=Analyzer.CHOICES)

    class Meta:
        model = Analyzer
        fields = ("method", "text")
        extra_kwargs = {'text': {'min_length': 20}}
