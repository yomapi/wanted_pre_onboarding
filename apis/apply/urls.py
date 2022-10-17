from django.urls import path
from .apis import WantedAPI, create_application, WantedDetailApi

urlpatterns = [
    path("application/", create_application),
    path("wanted/", WantedAPI.as_view()),
    path("wanted/<wanted_id>", WantedDetailApi.as_view()),
]
