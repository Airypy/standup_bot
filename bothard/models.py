from django.db import models

# Create your models here.
class Report(models.Model):
    user=models.CharField(max_length=100,primary_key=True)
    today=models.CharField(max_length=400,null=True)
    yesterday=models.CharField(max_length=400,null=True)
    obstacles=models.CharField(max_length=400,null=True)

    def __str__(self):
        return str(self.user)
