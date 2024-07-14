from django.db import models

# Create your models here.


class Mark(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    producer_country_name = models.CharField(max_length=50)
    is_visible = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['producer_country_name']),
        ]

    def __str__(self):
        return self.name


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mark_id = models.ForeignKey(Mark, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mark_id = models.ForeignKey(Mark, on_delete=models.CASCADE)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.FloatField()
    json_data = models.JSONField(default=dict)
    is_visible = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_visible']),
            models.Index(fields=['json_data']),
        ]

    def __str__(self):
        return self.name
