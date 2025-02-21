from django.conf import settings
import json
from django.views import View
from redis_om import NotFoundError

from .models import ActionLog
from .serializers import serialize_dataclass
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class ActionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        actionlogs: list[ActionLog] = ActionLog.find(ActionLog.user_id == request.user.id).sort_by('date').all()
        return JsonResponse(data=serialize_dataclass(actionlogs), safe=False)

    def delete(self, request, *args, **kwargs):
        ActionLog.find().delete()
        return JsonResponse(data={'result': 'Ok'})

    def post(self, request, *args, **kwargs):
        actionlog = ActionLog(user_id=request.user.id, **json.loads(request.body.decode('utf-8')))
        actionlog.save()
        actionlog.expire(settings.ACTIONLOG_TTL)
        return JsonResponse(data=serialize_dataclass(actionlog))


class ActionDetailView(LoginRequiredMixin, View):

    @property
    def action_id(self):
        return self.kwargs['action_id']

    def get(self, request, *args, **kwargs):
        actionlog = ActionLog.get(self.action_id)
        return JsonResponse(data=serialize_dataclass(actionlog))

    def put(self, request, *args, **kwargs):
        actionlog = ActionLog.get(self.action_id)
        if actionlog.user_id != request.user.id:
            raise NotFoundError()
        actionlog.update(**json.loads(request.body.decode('utf-8')))
        actionlog.expire(settings.ACTIONLOG_TTL)
        return JsonResponse(data=serialize_dataclass(actionlog))

    def delete(self, request, *args, **kwargs):
        ActionLog.delete(self.action_id)
        return JsonResponse(data={'result': 'Ok'})
