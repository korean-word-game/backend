from django.db import models


class WordFile(models.Model):
    file = models.FileField(null=True, upload_to='')

    def __str__(self):
        return self.file.name


class WordType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Word(models.Model):
    type = models.ForeignKey(WordType, on_delete=models.CASCADE)
    text = models.TextField()
    info = models.TextField(blank=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.text


class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.TextField(max_length=1000)
    nickname = models.CharField(max_length=50)
    token = models.TextField()

    def __str__(self):
        return self.username
