from rest_framework import serializers
from apply.models import Wanted
from apply.serializers import WantedListSerializer, WantedSerializer


class CreateApplicationReqSchema(serializers.Serializer):
    wanted_id = serializers.IntegerField(help_text="채용공고 id")
    applicant_id = serializers.IntegerField(help_text="사용자 id")


class CreateWantedReqSchema(serializers.ModelSerializer):
    class Meta:
        model = Wanted
        fields = [
            "title",
            "country",
            "location",
            "role",
            "reward",
            "tech_stack_name",
            "contents",
            "company",
        ]


class GetWantedResSchema(WantedSerializer):
    ohter_watned = serializers.ListField(child=WantedListSerializer())
