from django.urls import path

from actionlog.views import ActionDetailView, ActionListView

urlpatterns = [
    path("", ActionListView.as_view()),
    path("/<str:action_id>", ActionDetailView.as_view()),
]
