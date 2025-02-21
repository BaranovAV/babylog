from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pathlib


urlpatterns = [
    path('api/actions/', include('actionlog.urls')),
    path('', login_required(lambda r: HttpResponse(pathlib.Path('core/templates/main.html').read_text())), name='main'),
    path('lgn/', LoginView.as_view(template_name='login.html', next_page='main'), name='login'),
]
