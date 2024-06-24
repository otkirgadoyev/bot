from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.TextChoices):
    yuridik = "юридический", _("юридический")
    kadr = "кадр", _("кадр")  # Xodimlar
    buxgalter = "бухгалтер", _("бухгалтер")  # Bo'lim boshlig'i
    pochta = "входящая_исходящая_почта", _("входящая исходящая почта")  # Rahbarlar
