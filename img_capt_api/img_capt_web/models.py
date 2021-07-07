from django.db import models


class Folder(models.Model):
    path = models.CharField(max_length=100)

    def __str__(self):
        return self.path


class Image(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    path = models.CharField(max_length=100)
    data = models.CharField(max_length=500)

    def __str__(self):
        return self.path
