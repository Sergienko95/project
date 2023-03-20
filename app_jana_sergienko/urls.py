from django.urls import path

from app_jana_sergienko import contacts
from app_jana_sergienko import profile
from app_jana_sergienko import tag
from app_jana_sergienko import views

urlpatterns = [
    path("", views.helloworld),
    path("average/", views.handle_average),
    path("avgForm/", views.AverView.as_view()),
    path("classAverage/", views.AverageView.as_view()),
    path("contacts/", contacts.ContactListView.as_view()),
    path(
        "contacts/<int:contact_pk>/tags/<int:tag_pk>/assign/",
        tag.TagContactAssignView.as_view(),
    ),
    path(
        "contacts/<int:contact_pk>/tags/<int:tag_pk>/unassign/",
        tag.TagContactUnassignView.as_view(),
    ),
    path("contacts/<int:contact_pk>/tags/add/", tag.TagCreateView.as_view()),
    path("contacts/<int:pk>/", contacts.ContactDetailsView.as_view()),
    path("contacts/<int:pk>/delete/", contacts.ContactDeleteView.as_view()),
    path("contacts/<int:pk>/update/", contacts.ContactUpdateView.as_view()),
    path("contacts/add/", contacts.ContactCreateView.as_view()),
    path("contacts/search/", contacts.SearchResultsView.as_view()),
    path(
        "contacts/search/tags/<int:tag_pk>/assign/",
        tag.TagSearchAssignView.as_view(),
    ),
    path(
        "contacts/search/tags/<int:tag_pk>/unassign/",
        tag.TagSearchUnassignView.as_view(),
    ),
    path("profile/", profile.ProfileDetailsView.as_view()),
    path("profile/update/", profile.ProfileUpdateView.as_view()),
    path("lesson04/task01/", views.handle_task_01_money),
    path("lesson04/task02/", views.handle_task_02_sign),
    path("lesson04/task03/", views.handle_task_03_triangle),
    path("lesson04/task04/", views.handle_task_04_palindrom),
]
