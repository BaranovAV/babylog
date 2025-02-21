import datetime
from redis_om import HashModel, Migrator, Field
from django.core.cache import cache


class ActionLog(HashModel):
    type_name: str
    date: datetime.datetime = Field(sortable=True, index=True)
    user_id: int = Field(index=True)
    comment: str

    class Meta:
        global_key_prefix = 'actionlog'

        @classmethod
        @property
        def database(cls):
            return cache.client.get_client(write=True)


Migrator().run()