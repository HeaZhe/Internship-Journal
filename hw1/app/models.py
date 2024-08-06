
from django.db import models


class Context(models.Model):
    Context_text = models.CharField(max_length=200)
    Created_date = models.DateTimeField('date_created')
    Delete_date = models.DateTimeField('date_deleted', null=True, blank=True)
    def __str__(self):
        return self.Context_text