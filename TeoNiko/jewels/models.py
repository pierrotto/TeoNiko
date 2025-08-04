from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from TeoNiko.jewels.choices import GemShapeChoices, GemColorChoices, JewelCategoryChoices


UserModel = get_user_model()


class Jewel(models.Model):
    name = models.CharField(
        max_length=30,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    weave_technique = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    name = models.CharField(
        choices=JewelCategoryChoices,
    )

    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(
        upload_to='uploads/photos/',
    )

    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    date_uploaded = models.DateTimeField(
        auto_now_add=True,
    )

    jewel = models.ForeignKey(
        'Jewel',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
    )

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
    )

    uploaded_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='photos',
    )

    is_admin_uploaded = models.BooleanField(
        default=True
    )


class Collection(models.Model):
    name = models.CharField(
        max_length=30,
    )

    description = models.CharField(
        max_length=100,
    )

    jewels = models.ManyToManyField(
        'Jewel',
        related_name='collections',
    )


class Metal(models.Model):
    type = models.CharField(
        max_length=30,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
    )

    jewel = models.ManyToManyField(
        to='Jewel',
        related_name='metals',
    )


class Gem(models.Model):
    type = models.CharField(
        max_length=30,
    )

    color = models.CharField(
        choices=GemColorChoices,
        default=GemColorChoices.OTHER
    )

    shape = models.CharField(
        choices=GemShapeChoices,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
    )

    jewel = models.ManyToManyField(
        to='Jewel',
    )


class Material(models.Model):
    type = models.CharField(
        max_length=30,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
