from django.urls import path, include

urlpatterns = [
    path('api/actions/', include('actionlog.urls')),
]
