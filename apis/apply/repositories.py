from django.conf import settings

from apply.models import Wanted
from apply.serializers import WantedSerializer, WantedListSerializer
from exceptions import NotFoundError


class WantedRepo:
    def __init__(self) -> None:
        self.model = Wanted
        self.serilaizer = WantedSerializer
        self.list_serilaizer = WantedListSerializer

    def create(self, params: dict) -> dict:
        serializer = self.serilaizer(data=params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(self, wanted_id: int, params: dict):
        try:
            target = self.model.objects.get(id=wanted_id)
            serializer = self.serilaizer(target, data=params)
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
    ) -> list:
        query = self.model.objects.filter(**search_optons)
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
