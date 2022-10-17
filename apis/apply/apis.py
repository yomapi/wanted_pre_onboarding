from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from decotrators.exeception_handler import execption_hanlder
from decotrators.validate_required_keys import validate_required_keys
from django.http import JsonResponse
from apply.repositories import WantedRepo, ApplicationRepo

wanted_repo = WantedRepo()
application_repo = ApplicationRepo()


@api_view(["GET"])
@execption_hanlder()
def find_wanted_with_limit(request):
    return JsonResponse({"data": wanted_repo.find_with_limit()})


@parser_classes([JSONParser])
@execption_hanlder()
def find_wanted(request):
    return JsonResponse({"data": wanted_repo.find()})


@parser_classes([JSONParser])
@execption_hanlder()
def create_wanted(request):
    return JsonResponse({"data": wanted_repo.create(request.data)})


class WantedAPI(APIView):
    def get(self, request):
        return find_wanted(request)

    def post(self, request):
        return create_wanted(request)


@api_view(["GET"])
@parser_classes([JSONParser])
@execption_hanlder()
def get_wanted(request, wanted_id):
    wanted = wanted_repo.get(wanted_id)
    wanted["ohter_watned"] = wanted_repo.find_with_limit(
        search_optons={"company": wanted["company"]}, exclude_id=wanted_id
    )
    return JsonResponse({"data": wanted})


@api_view(["POST"])
@parser_classes([JSONParser])
@execption_hanlder()
@validate_required_keys(["wanted_id", "applicant_id"])
def create_application(request):
    params = request.data
    return JsonResponse(
        {
            "data": application_repo.create(
                wanted_id=params["wanted_id"], applicant_id=params["applicant_id"]
            )
        }
    )
