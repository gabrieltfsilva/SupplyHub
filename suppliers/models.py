from django.db import models
from django.contrib.auth.models import User

# Subcategory model. Linked to a predefined set of static categories.
class Subcategory(models.Model):
    CATEGORY_CHOICES = [
        ('diversos', 'Diversos'),
        ('equipamentos', 'Equipamentos'),
        ('logistica', 'Logística'),
        ('materiais', 'Materiais'),
        ('servicos', 'Serviços'),
        ('softwares', 'Softwares'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_category_display()} > {self.name}"

    class Meta:
        unique_together = ('category', 'name')
        verbose_name_plural = "Subcategories"

# Supplier model.
class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name='suppliers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Review model.
class Review(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('supplier', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.supplier.name} ({self.rating})"
