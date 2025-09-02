from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from TeoNiko.jewels.choices import GemShapeChoices, GemColorChoices, JewelCategoryChoices, JewelMaterialChoices, \
    GemTypeChoices, JewelMetalChoices

UserModel = get_user_model()


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


class Jewel(models.Model):
    name = models.CharField(
        max_length=30,
    )

    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )

    short_description = models.TextField(
        max_length=250,
        blank=True
    )

    long_description = models.TextField(
        max_length=1500,
        blank=True
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

    rating_avg = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    rating_count = models.PositiveIntegerField(
        default=0
    )

    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_available = models.BooleanField(
        default=True,
    )

    code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:140] or "item"
            slug = base
            i = 2
            Model = type(self)
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix = f"-{i}"
                slug = f"{base[:140 - len(suffix)]}{suffix}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def cover_photo(self):
        p = self.photos.filter(is_cover=True).first()
        return p or self.photos.order_by("sort_order", "id").first()


class Photo(models.Model):
    sort_order = models.PositiveIntegerField(default=0, db_index=True)

    image = models.ImageField(
        upload_to='uploads/photos/',
    )

    is_cover = models.BooleanField(default=False)

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

    jewel_set = models.ForeignKey(
        'JewelSet',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='photos',
    )

    class Meta:
        ordering = ["sort_order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["jewel"], condition=Q(is_cover=True),
                name="one_cover_photo_per_jewel",
            ),
            models.UniqueConstraint(
                fields=["collection"], condition=Q(is_cover=True),
                name="one_cover_photo_per_collection",
            ),
            models.UniqueConstraint(
                fields=["category"], condition=Q(is_cover=True),
                name="one_cover_photo_per_category",
            ),
            # NEW:
            models.UniqueConstraint(
                fields=["jewel_set"], condition=Q(is_cover=True),
                name="one_cover_photo_per_jewel_set",
            ),
        ]

    def clean(self):
        owners = [self.jewel, self.category, self.collection, self.jewel_set]
        if sum(o is not None for o in owners) != 1:
            raise ValidationError("Attach a photo to exactly one of: jewel, category, collection, or jewel_set.")


class JewelSpec(models.Model):
    jewel = models.ForeignKey(Jewel, on_delete=models.CASCADE, related_name="specs")
    label = models.CharField(max_length=80, null=True, blank=True)  # left part
    value = models.TextField(max_length=1500)  # right part
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class JewelTab(models.Model):
    jewel = models.ForeignKey(Jewel, on_delete=models.CASCADE, related_name="tabs")
    title = models.CharField(max_length=80)
    body_en = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.jewel.name} · {self.title}"


class Collection(models.Model):
    name = models.CharField(
        max_length=30,
    )

    description = models.CharField(
        max_length=100,
    )

    rating_avg = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )

    rating_count = models.PositiveIntegerField(
        default=0
    )

    jewels = models.ManyToManyField(
        'Jewel',
        related_name='collections',
    )

    sets = models.ManyToManyField('JewelSet', related_name='collections', blank=True, )

    def __str__(self):
        return self.name


class Metal(models.Model):
    type = models.CharField(
        max_length=30,
        choices=JewelMetalChoices,
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
        choices=GemTypeChoices
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
        related_name='gems',
    )


class Material(models.Model):
    type = models.CharField(
        max_length=30,
        choices=JewelMaterialChoices,
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=3,
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    jewel = models.ManyToManyField(
        to='Jewel',
        related_name='materials',
    )


class JewelSet(models.Model):
    name = models.CharField(
        max_length=60
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        null=True,
        db_index=True)

    short_description = models.TextField(
        max_length=250,
        blank=True)
    long_description = models.TextField(
        max_length=1500,
        blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    rating_avg = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0)

    rating_count = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    code = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    jewels = models.ManyToManyField(
        'Jewel',
        through='JewelSetItem',
        related_name='in_sets',
        blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:100] or "set"
            slug = base
            i = 2
            Model = type(self)
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix = f"-{i}"
                slug = f"{base[:140 - len(suffix)]}{suffix}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def cover_photo(self):
        p = self.photos.filter(is_cover=True).first()
        return p or self.photos.order_by("sort_order", "id").first()

    @property
    def categories(self):
        # Distinct list of category names of items inside the set
        return list(self.jewels.values_list('category__name', flat=True).distinct())


class JewelSetItem(models.Model):
    jewel_set = models.ForeignKey(
        JewelSet,
        on_delete=models.CASCADE,
        related_name='items'
    )

    jewel = models.ForeignKey(
        'Jewel',
        on_delete=models.PROTECT,
        related_name='set_items'
    )

    quantity = models.PositiveSmallIntegerField(
        default=1
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True
    )

    class Meta:
        unique_together = [('jewel_set', 'jewel')]
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.jewel_set.name}: {self.quantity} × {self.jewel.name}"
