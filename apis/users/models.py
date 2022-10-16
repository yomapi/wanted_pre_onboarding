from django.db import models
from apis.models import BaseModel


class UserBase(BaseModel):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)

    class Meta:
        abstract = True
        managed = False


class Applicant(UserBase):
    class Meta:
        db_table = "applicant"


class Company(UserBase):
    class Meta:
        db_table = "company"
