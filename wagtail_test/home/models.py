from sre_parse import CATEGORIES
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django import forms

from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting


from home import blocks

class BlogCategory(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='Un slug para identificar las categorias',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


register_snippet(BlogCategory)

class HomePage(RoutablePageMixin, Page):

    templates = "home/home_page.html"
    max_count = 1
    
    sub_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    
    page_logo =  models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        ImageChooserPanel("page_logo"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public().order_by("last_published_at")
        all_posts = context["posts"]
        if request.GET.get('category', None):
            category = request.GET.get('category')
            all_posts = all_posts.filter(categories_post__slug__in=[category])
        elif request.GET.get('search', None):
            search = request.GET.get('search', None)
            all_posts = all_posts.filter(title__icontains=search)
        else:
            all_posts = context["posts"]
        # Paginate all posts by 2 per page
        
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists, return it
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the page doesn't exist, return the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the page is out of range (e.g. 9999), return the last page
            posts = paginator.page(paginator.num_pages)

        # Add the posts to the context
        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()
        return context
    
    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        # Find the category in all posts
        context = self.get_context(request)

        try:
            # Get the category posts
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            # If the category doesn't exist, set category to None
            category = None

        if category is None:
            # if the category is None, return all posts
            return render(request, "home/home_page.html", context)

        context["posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])

        # Add the category to the context so we can use it in the template
        return render(request, "home/home_page.html", context)

    class Meta:
        ordering = ["last_published_at"]


class BlogDetailPage(Page):

    blog_resume = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Change the default title',
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    
    categories_post = ParentalManyToManyField("home.BlogCategory", blank=True)

    content = StreamField(
        [
            ("full_richtext", blocks.RichtextBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("blog_resume"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel (
            [
                FieldPanel("categories_post", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categorias"
        ),
        StreamFieldPanel("content"),
    ]
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["categories"] = BlogCategory.objects.all()
        return context
    
    def prev_portrait(self):
        if self.get_prev_sibling():
            return self.get_prev_sibling().url
        else:
            return self.get_siblings().last().url

    def next_portrait(self):
        if self.get_next_sibling():
            return self.get_next_sibling().url
        else:
            return self.get_siblings().first().url
    
@register_setting
class BusinessSettings(BaseSetting):
    """Configuraciones de la empresa"""

    page_logo =  models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    panels = [
        MultiFieldPanel([
            ImageChooserPanel("page_logo"),
        ], heading="Configuracion de la Empresa")
    ]
    
    def __str__(self) -> str:
        return "Configuraciones de la Empresa"