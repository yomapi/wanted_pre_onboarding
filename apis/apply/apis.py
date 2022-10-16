from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


from django.http import JsonResponse
from apply.repositories import WantedRepo

wanted_repo = WantedRepo()


@api_view(["GET"])
def find_wanted_with_limit(request):
    return JsonResponse({"data": wanted_repo.find_with_limit()})


def find_wanted(request):
    return JsonResponse({"data": wanted_repo.find()})


@parser_classes([JSONParser])
def create_wanted(request):
    return JsonResponse({"data": wanted_repo.create(request.data)})


class WantedAPI(APIView):
    def get(self, request):
        return find_wanted(request)

    def post(self, request):
        return create_wanted(request)
