from django.urls import path
from actionlog.views import ActionListView, ActionDetailView

urlpatterns = [
    path('', ActionListView.as_view()),
    path('<int:action_id>', ActionDetailView.as_view()),
]
