from django.db import models
class SexOptions(models.TextChoices):
    male = 'Male'
    female = 'Female'
    not_informed = 'Not Informed'

class Pet (models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices= SexOptions.choices,
        default = SexOptions.not_informed
    )
    group = models.ForeignKey('groups.Group',on_delete=models.PROTECT, related_name= 'pets')

