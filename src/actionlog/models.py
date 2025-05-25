import datetime

from redis_om import Field, HashModel


class ActionLog(HashModel):
    type_name: str
    date: datetime.datetime = Field(sortable=True, index=True)
    user_id: int = Field(index=True)
    comment: str

    class Meta:
        global_key_prefix = "actionlog"
