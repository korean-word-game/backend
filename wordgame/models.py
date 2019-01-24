from django.db import models


class HowToWin(models.Model):
    name = models.CharField(max_length=10)
    info = models.TextField()

    def __str__(self):
        return self.name


class Mode(models.Model):
    name = models.CharField(max_length=10)
    info = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=20)
    mode = models.ForeignKey(
        Mode,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    how_to_win = models.ForeignKey(
        HowToWin,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_hide = models.BooleanField()
    now_people = models.IntegerField(default=1)
    is_start = models.BooleanField(default=False)

    def __str__(self):
        return self.title
