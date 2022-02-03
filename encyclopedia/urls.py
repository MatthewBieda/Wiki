from random import random
from django.urls import path

from . import views

#This file simply performs URL routing, no complex logic should go here. 

urlpatterns = [
    path(
        route="",
        view=views.index,
        name="index"
    ),
    path(
        route="wiki/<str:entry>",
        view=views.entry,
        name="entry"
    ),
    path(
        route="wiki/<str:entry>/edit",
        view=views.edit,
        name="edit"
    ),
    path(
        route="search",
        view=views.search,
        name="search"
    ),
    path(
        route="newpage",
        view=views.newpage,
        name="newpage"
    ),
    path(
        route="savepage",
        view=views.savepage,
        name="savepage"
    ),
    path(
        route="random",
        view=views.random,
        name="random"
    ),
    path(
        route="saveedit",
        view=views.saveedit,
        name="saveedit"
    )
]
