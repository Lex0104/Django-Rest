import re

from rest_framework.serializers import ValidationError


class LinkToVideo:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/')
        url = dict(value).get(self.field)
        if not bool(reg.match(url)):
            raise ValidationError('Разрешены только ссылки на youtube.com или youtu.be')