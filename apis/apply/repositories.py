from typing import Union
from django.conf import settings
from rest_framework.exceptions import ValidationError
from apply.models import Wanted, Application
from apply.serializers import (
    WantedSerializer,
    WantedListSerializer,
    ApplicationSerializer,
)
from exceptions import NotFoundError, DuplicatedApplicationError


class WantedRepo:
    def __init__(self) -> None:
        self.model = Wanted
        self.serilaizer = WantedSerializer
        self.list_serilaizer = WantedListSerializer

    def get(self, wanted_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(id=wanted_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, params: dict) -> dict:
        serializer = self.serilaizer(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(self, wanted_id: int, params: dict):
        try:
            target = self.model.objects.get(id=wanted_id)
            if params.get("company", False) and target.company != params["company"]:
                raise ValidationError("You can't update company ID")
            serializer = self.serilaizer(target, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise NotFoundError
        return serializer.data

    def delete(self, wanted_id: int):
        try:
            target = self.model.objects.get(id=wanted_id)
            target.delete()
            return True
        except self.model.DoesNotExist:
            raise NotFoundError

    def count_with_options(self, search_optons: dict = {}) -> int:
        query = self.model.objects.filter(**search_optons)
        return query.count()

    def find_with_limit(
        self,
        offset: int = 0,
        limit: int = settings.DEFAULT_FIND_LIMIT,
        search_optons: dict = {},
        exclude_id: Union[int, None] = None,
    ) -> list:
        query = self.model.objects.filter(**search_optons)
        query = query.exclude(id=exclude_id) if exclude_id != None else query
        return WantedListSerializer(
            query[offset : limit + offset],
            many=True,
        ).data

    def find(
        self,
        search_optons: dict = {},
    ) -> list:
        return WantedListSerializer(
            self.model.objects.filter(**search_optons),
            many=True,
        ).data


class ApplicationRepo:
    def __init__(self) -> None:
        self.model = Application
        self.serializer = ApplicationSerializer

    def create(self, wanted_id: int, applicant_id: int):
        try:
            self.model.objects.get(wanted=wanted_id, applicant=applicant_id)
            raise DuplicatedApplicationError
        except self.model.DoesNotExist:
            serializer = self.serializer(
                data={"wanted": wanted_id, "applicant": applicant_id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
