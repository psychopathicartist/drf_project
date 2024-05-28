import re
from rest_framework import serializers


class VideoUrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('https://www.youtube.com')
        if value.get(self.field):
            tmp_val = dict(value).get(self.field)
            if not bool(reg.match(tmp_val)):
                raise serializers.ValidationError('Ресурсом для ссылки видео может быть только платформа YouTube')
        else:
            return None
