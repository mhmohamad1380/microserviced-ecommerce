from django.db import models

class Cart(models.Model):
    user = models.PositiveIntegerField(blank=False, null=True)
    product = models.PositiveIntegerField(blank=False, null=True)
    detail_index = models.PositiveSmallIntegerField(blank=False, default=0)
    count = models.PositiveIntegerField(blank=False, default=1)

    def __str__(self) -> str:
        return f"{self.user} | {self.product}"
