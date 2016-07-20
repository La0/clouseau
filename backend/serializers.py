from flask.json import JSONEncoder
from datetime import timedelta


class TimedeltaJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, timedelta):
                return obj.total_seconds()

            iterable = iter(obj)
        except TypeError:
            pass

        else:
            return list(iterable)

        return JSONEncoder.default(self, obj)

