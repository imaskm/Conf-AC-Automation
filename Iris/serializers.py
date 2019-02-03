from django.core.serializers import serialize
from .models import *


class MasterSerializer:

    def get_json_serialzed_obj(self):
        return serialize('json', Master)