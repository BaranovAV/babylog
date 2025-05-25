import json

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from redis_om import NotFoundError

from .models import ActionLog


class ActionListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        action_logs: list[ActionLog] = (
            ActionLog.find(ActionLog.user_id == request.user.id).sort_by("date").all()
        )
        return JsonResponse(data=[log.model_dump() for log in action_logs], safe=False)

    def delete(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponse:
        ActionLog.find().delete()
        return JsonResponse(data={"result": "Ok"})

    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        action_log = ActionLog(
            user_id=request.user.id, **json.loads(request.body.decode("utf-8"))
        )
        action_log.save()
        action_log.expire(settings.ACTIONLOG_TTL)
        return JsonResponse(data=action_log.model_dump())


class ActionDetailView(LoginRequiredMixin, View):

    @property
    def action_id(self) -> str:
        return self.kwargs["action_id"]

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        action_log = ActionLog.get(self.action_id)
        return JsonResponse(data=action_log.model_dump())

    def put(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        action_log = ActionLog.get(self.action_id)
        if action_log.user_id != request.user.id:
            raise NotFoundError()
        action_log.update(**json.loads(request.body.decode("utf-8")))
        action_log.expire(settings.ACTIONLOG_TTL)
        return JsonResponse(data=action_log.model_dump())

    def delete(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> HttpResponse:
        ActionLog.delete(self.action_id)
        return JsonResponse(data={"result": "Ok"})
