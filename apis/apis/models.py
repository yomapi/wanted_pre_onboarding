from django.db import models


class BaseModel(models.Model):
    using = "wanted_pre_onboarding"
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        managed = False
