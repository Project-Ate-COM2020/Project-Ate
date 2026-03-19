from django.contrib.auth import get_user_model
from django.db import models


class Maintainer(models.Model):
    maintainer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "maintainer"
