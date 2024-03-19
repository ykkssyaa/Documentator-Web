import os
from django.db import models


def doc_file_path(instance, filename):
    number = instance.number
    _, file_extension = os.path.splitext(filename)
    return f'docs/{number}{file_extension}'


class Document(models.Model):
    title = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField()

    STATUS_CHOICES = [
        ('В обработке', 'В обработке'),
        ('Подписан', 'Подписан'),
        ('В исполнении', 'В исполнении'),
        ('Завершен', 'Завершен'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    file = models.FileField(upload_to=doc_file_path, null=True)

    signing_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/documents/{self.number}'


class Duty(models.Model):
    title = models.CharField(max_length=100)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
