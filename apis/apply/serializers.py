from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Wanted, Application


class WantedSerializer(serializers.ModelSerializer):
    def validate_reward(self, value):
        if value < 0:
            raise ValidationError("rewards have to be equal or bigger than 0")
        return value

    class Meta:
        model = Wanted
        fields = "__all__"


class WantedListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name")

    class Meta:
        model = Wanted
        fields = [
            "id",
            "company_name",
            "title",
            "country",
            "location",
            "role",
            "reward",
            "tech_stack_name",
            "updated_at",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
