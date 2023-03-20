from django.urls import path

from app_jana_sergienko import contacts
from app_jana_sergienko import profile
from app_jana_sergienko import tag

urlpatterns = [
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
]
