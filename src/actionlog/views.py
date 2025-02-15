from django.conf import settings
import datetime
import json
from django.views import View
from django.core.cache import cache
from .models import ActionLog
from .serializers import serialize_dataclass
from django.http import JsonResponse


def _create_or_update(request, id, *args, **kwargs):
    actionlog_kwargs = {
        **json.loads(request.body.decode('utf-8')),
        'id': id
    }
    actionlog = ActionLog(**actionlog_kwargs)
    cache.set(f'data:{actionlog.id}', actionlog, timeout=settings.ACTIONLOG_TTL)
    return JsonResponse(data=serialize_dataclass(actionlog))


class ActionListView(View):

    def get(self, request, *args, **kwargs):
        actionlogs: list[ActionLog] = [cache.get(k) for k in cache.keys('data:*')]
        return JsonResponse(data=serialize_dataclass(actionlogs), safe=False)

    def delete(self, request, *args, **kwargs):
        cache.delete_pattern('data:*')
        return JsonResponse(data={'result': 'Ok'})

    def post(self, request, *args, **kwargs):
        return _create_or_update(request, *args, id=int(datetime.datetime.now().timestamp()*1000), **kwargs)


class ActionDetailView(View):

    def put(self, request, *args, **kwargs):
        return _create_or_update(request, *args, id=self.kwargs['action_id'], **kwargs)

    def delete(self, request, *args, **kwargs):

        cache.delete(f"data:{self.kwargs['action_id']}")
        return JsonResponse(data={'result': 'Ok'})
