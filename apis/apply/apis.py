from rest_framework.decorators import api_view, parser_classes
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from apply.serializers import WantedListSerializer
from decotrators.exeception_handler import execption_hanlder
from decotrators.validate_required_keys import validate_required_keys
from django.http import JsonResponse
from apply.repositories import WantedRepo, ApplicationRepo
from drf_yasg.utils import swagger_auto_schema
from apply.serializers import (
    ApplicationSerializer,
    WantedSerializer,
    WantedListSerializer,
)
from apply.schemas import (
    CreateWantedReqSchema,
    CreateApplicationReqSchema,
    GetWantedResSchema,
)


wanted_repo = WantedRepo()
application_repo = ApplicationRepo()


@parser_classes([JSONParser])
@execption_hanlder()
def find_wanted(request):
    return JsonResponse(wanted_repo.find(), safe=False)


@parser_classes([JSONParser])
@execption_hanlder()
def create_wanted(request):
    return JsonResponse(wanted_repo.create(request.data))


class WantedAPI(APIView):
    @swagger_auto_schema(
        responses={200: WantedListSerializer(many=True)},
    )
    def get(self, request):
        return find_wanted(request)

    @swagger_auto_schema(
        request_body=CreateWantedReqSchema,
        responses={201: WantedSerializer},
    )
    def post(self, request):
        return create_wanted(request)


@swagger_auto_schema(
    method="get",
    responses={200: GetWantedResSchema},
)
@api_view(["GET"])
@parser_classes([JSONParser])
@execption_hanlder()
def get_wanted(request, wanted_id):
    wanted = wanted_repo.get(wanted_id)
    wanted["ohter_watned"] = wanted_repo.find_with_limit(
        search_optons={"company": wanted["company"]}, exclude_id=wanted_id
    )
    return JsonResponse(wanted, safe=False)


@swagger_auto_schema(
    method="post",
    request_body=CreateApplicationReqSchema,
    responses={201: ApplicationSerializer},
)
@api_view(["POST"])
@parser_classes([JSONParser])
@execption_hanlder()
@validate_required_keys(["wanted_id", "applicant_id"])
def create_application(request):
    params = request.data
    return JsonResponse(
        application_repo.create(
            wanted_id=params["wanted_id"], applicant_id=params["applicant_id"]
        )
    )
