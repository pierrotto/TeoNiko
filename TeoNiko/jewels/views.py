from decimal import Decimal, InvalidOperation, ROUND_FLOOR, ROUND_CEILING
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min, Max, Prefetch
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from TeoNiko.jewels.forms import JewelAddForm
from TeoNiko.jewels.mixins import StaffRequiredMixin
from TeoNiko.jewels.choices import GemColorChoices, JewelMaterialChoices, JewelMetalChoices
from TeoNiko.jewels.models import Category, Jewel, Photo, Gem, Material, Metal, JewelSpec, JewelTab
from django.shortcuts import get_object_or_404, redirect
from TeoNiko.jewels.templatetags.money import RATE as EUR_BGN_RATE


class CategoryLandingPageView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'jewels/category-landing-page.html'
    paginate_by = 6

    def get_queryset(self):
        return (
            Category.objects.order_by("name")
            .prefetch_related(
                Prefetch(
                    "photos",
                    queryset=Photo.objects.order_by("id"),
                    to_attr="photos_sorted"
                )
            )
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        agg = Jewel.objects.aggregate(min_price=Min("price"), max_price=Max("price"))
        pmin = agg["min_price"] or 0
        pmax = agg["max_price"] or 0

        ctx.update({
            "price_min": pmin,
            "price_max": pmax,
            "min": pmin,
            "max": pmax,
            "disable_submit": True,
        })
        return ctx


class CategoryFilterView(ListView):
    model = Jewel
    context_object_name = 'jewels'
    template_name = 'jewels/category.html'
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, name__iexact=kwargs.get('name'))
        base_qs = Jewel.objects.filter(category=self.category)
        bounds = base_qs.aggregate(lo=Min('price'), hi=Max('price'))
        self.price_min = bounds['lo'] if bounds['lo'] is not None else 0
        self.price_max = bounds['hi'] if bounds['hi'] is not None else 0
        return super().dispatch(request, *args, **kwargs)

    def _to_dec(self, val):
        if val in (None, ""):
            return None
        val = str(val).replace(",", ".")
        try:
            return Decimal(val)
        except (InvalidOperation, ValueError, TypeError):
            return None

    def _selected_range(self):
        lo = Decimal(self.price_min)
        hi = Decimal(self.price_max)
        sel_min = self._to_dec(self.request.GET.get('min')) or lo
        sel_max = self._to_dec(self.request.GET.get('max')) or hi
        sel_min = max(lo, sel_min)
        sel_max = min(hi, sel_max)
        if sel_min > sel_max:
            sel_min, sel_max = lo, hi
        q = Decimal('0.01')
        sel_min = sel_min.quantize(q, rounding=ROUND_FLOOR)
        sel_max = sel_max.quantize(q, rounding=ROUND_CEILING)
        return sel_min, sel_max

    def get_queryset(self):
        qs = (Jewel.objects.select_related('category')
              .prefetch_related('gems')
              .filter(category=self.category))

        sel_min, sel_max = self._selected_range()

        qs = qs.filter(price__gte=sel_min, price__lte=sel_max)

        stone = (self.request.GET.get('stone') or '').strip()
        if stone:
            qs = qs.filter(gems__type__iexact=stone)

        color = (self.request.GET.get('color') or '').strip()
        if color:
            qs = qs.filter(gems__color=color)

        mm = (self.request.GET.get('mm') or '').strip()
        if mm:
            try:
                kind, val = mm.split(':', 1)
            except ValueError:
                kind, val = '', mm
            if kind == 'metal':
                qs = qs.filter(metals__type__iexact=val)
            elif kind == 'material':
                qs = qs.filter(materials__type=val)

        order = self.request.GET.get('order')
        order_map = {"newest": "-id", "price_asc": "price", "price_desc": "-price"}
        if order in order_map:
            qs = qs.order_by(order_map[order])

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        sel_min, sel_max = self._selected_range()

        ctx.update({
            "categories": Category.objects.order_by("name"),
            "current_category": self.category,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "min": sel_min,
            "max": sel_max,
            "order": self.request.GET.get("order", "newest"),
            "price_disabled": (self.price_min == self.price_max == 0),
        })

        stones_qs = (
            Gem.objects
            .filter(jewel__category=self.category)
            .values_list("type", flat=True)
            .exclude(type__isnull=True)
            .exclude(type__exact="")
            .distinct()
            .order_by("type")
        )
        ctx["stones"] = list(stones_qs)
        ctx["stone"] = (self.request.GET.get("stone") or "").strip()

        color_values = (Gem.objects
                        .filter(jewel__category=self.category)
                        .values_list('color', flat=True)
                        .exclude(color__isnull=True)
                        .exclude(color__exact='')
                        .distinct())

        labels_map = dict(GemColorChoices.choices)
        colors = [(val, labels_map.get(val, val)) for val in color_values]
        colors.sort(key=lambda t: t[1])
        ctx["colors"] = colors
        ctx["color"] = (self.request.GET.get("color") or "").strip()

        metal_vals = (Metal.objects
                      .filter(jewel__category=self.category)
                      .values_list('type', flat=True)
                      .exclude(type__isnull=True)
                      .exclude(type__exact='')
                      .distinct())
        metal_label_map = dict(JewelMetalChoices.choices)
        metals = []
        for v in metal_vals:
            label = metal_label_map.get(v, str(v).replace('_', ' ').upper())
            metals.append((v, label))
        metals.sort(key=lambda t: t[1])

        material_vals = (Material.objects
                         .filter(jewel__category=self.category)
                         .values_list('type', flat=True)
                         .exclude(type__isnull=True)
                         .exclude(type__exact='')
                         .distinct())
        material_label_map = dict(JewelMaterialChoices.choices)
        materials = [(v, material_label_map.get(v, v)) for v in material_vals]
        materials.sort(key=lambda t: t[1])

        ctx["metals"] = metals
        ctx["materials"] = materials
        ctx["mm"] = (self.request.GET.get("mm") or "").strip()

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["qs"] = params.urlencode()

        return ctx


class JewelCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Jewel
    form_class = JewelAddForm
    template_name = 'jewels/create-jewel.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()

        photo_file = self.request.FILES.get("photo")
        if photo_file:
            Photo.objects.create(
                image=photo_file,
                description=form.cleaned_data.get("photo_description") or "",
                jewel=self.object,
                category=self.object.category,
                uploaded_by=self.request.user if self.request.user.is_authenticated else None,
                is_admin_uploaded=True,
            )

        return super().form_valid(form)

    def get_success_url(self):
        category_name = self.object.category.name
        return reverse("category-by-name", kwargs={"name": category_name})


photo_prefetch = Prefetch("photos", queryset=Photo.objects.order_by("sort_order", "id"))
specs_prefetch = Prefetch("specs", queryset=JewelSpec.objects.order_by("order", "id"))
tabs_prefetch  = Prefetch("tabs",  queryset=JewelTab.objects.order_by("order", "id"))

qs = (Jewel.objects
      .select_related("category")
      .prefetch_related(photo_prefetch, specs_prefetch, tabs_prefetch))

photo_prefetch = Prefetch("photos", queryset=Photo.objects.order_by("sort_order", "id"))
specs_prefetch = Prefetch("specs",  queryset=JewelSpec.objects.order_by("order", "id"))
tabs_prefetch  = Prefetch("tabs",   queryset=JewelTab.objects.order_by("order", "id"))

class JewelDetailView(DetailView):
    model = Jewel
    template_name = "jewels/jewel-details.html"
    queryset = (
        Jewel.objects
        .select_related("category")
        .prefetch_related(
            photo_prefetch, specs_prefetch, tabs_prefetch,
            "gems", "materials", "metals"
        )
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        photos = list(self.object.photos.all())
        ctx["categories"] = Category.objects.order_by("name")
        ctx["main_photo"] = photos[0] if photos else None
        ctx["thumbs"] = photos[1:9]
        ctx["materials"] = list(self.object.materials.values_list("type", flat=True))
        ctx["metals"]    = list(self.object.metals.values_list("type", flat=True))
        ctx["gems"]      = list(self.object.gems.values_list("type", flat=True))
        ctx["bgn_per_eur"] = EUR_BGN_RATE
        return ctx

class JewelQuickView(DetailView):
    model = Jewel
    template_name = "jewels/partials/quick-view.html"
    queryset = (
        Jewel.objects
        .select_related("category")
        .prefetch_related(
            photo_prefetch, specs_prefetch, tabs_prefetch,
            "gems", "materials", "metals"
        )
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["materials"] = list(self.object.materials.values_list("type", flat=True))
        ctx["metals"]    = list(self.object.metals.values_list("type", flat=True))
        ctx["gems"]      = list(self.object.gems.values_list("type", flat=True))
        ctx["bgn_per_eur"] = EUR_BGN_RATE
        return ctx
