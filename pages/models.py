from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email
