from django.urls import path
from .apis import WantedAPI

urlpatterns = [path("", WantedAPI.as_view())]
