from django.db import models


class VideoCardAbs(models.Model):
    name = models.CharField("Имя продукта", max_length=256, db_index=True)
    link = models.CharField("Ссылка на продукт", max_length=1024, db_index=True)
    price = models.CharField("Цена", max_length=30, db_index=True)
    available = models.BooleanField("Доступность", db_index=True)

    def __str__(self):
        return f"{self.name}"


class VcMV(VideoCardAbs):
    class Meta:
        verbose_name = "Видеокарта Мвидео"
        verbose_name_plural = "Видеокарты Мвидео"
        ordering = ["price"]


class VcCL(VideoCardAbs):
    class Meta:
        verbose_name = "Видеокарта Citilink"
        verbose_name_plural = "Видеокарты Citilink"
        ordering = ["price"]


class VcDNS(VideoCardAbs):
    class Meta:
        verbose_name = "Видеокарта DNS"
        verbose_name_plural = "Видеокарты DNS"
        ordering = ["price"]
