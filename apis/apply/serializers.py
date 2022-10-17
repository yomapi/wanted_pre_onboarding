from rest_framework import serializers
from .models import Wanted, Application


class WantedSerializer(serializers.ModelSerializer):
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
