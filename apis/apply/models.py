from django.db import models
from apis.models import BaseModel
from users.models import Applicant, Company


class Wanted(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name="company",
        on_delete=models.CASCADE,
        db_column="company_id",
    )
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    role = models.CharField(max_length=200)
    reward = models.PositiveIntegerField(null=False, default=0)
    tech_stack_name = models.CharField(max_length=200)
    contents = models.TextField()

    class Meta:
        db_table = "wanted"


class Application(BaseModel):
    wanted = models.ForeignKey(
        Wanted,
        related_name="wanted",
        on_delete=models.CASCADE,
        db_column="wanted_id",
    )
    applicant = models.ForeignKey(
        Applicant,
        related_name="applicant",
        on_delete=models.CASCADE,
        db_column="applicant_id",
    )

    class Meta:
        db_table = "application"
