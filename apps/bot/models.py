from django.db import models
from .choices import Category

class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Full name")
    phone_number = models.CharField(max_length=15, null=True, verbose_name="Phone number")
    telegram_id = models.CharField(max_length=15,verbose_name="Telegram id", null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"


class File(models.Model):

    category = models.CharField(max_length=100, null=True, choices=Category.choices)
    file = models.FileField(null=True, blank=True, verbose_name="File")

    def __str__(self):
        return str(self.file.name)

    class Meta:
        db_table = "files"
        verbose_name = "File"
        verbose_name_plural = "Files"
