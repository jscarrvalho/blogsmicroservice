from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True


class BlogPost(BaseModel):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{} - {}".format(self.title, self.date_posted)
