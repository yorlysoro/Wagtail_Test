from django.db import models

from wagtail.models import Page


class HomePage(Page):
    """Home Page model."""
    templates = "home/home_page.html"
