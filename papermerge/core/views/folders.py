

from papermerge.core.models import Folder
from rest_framework_json_api.views import ModelViewSet

from papermerge.core.serializers import FolderSerializer
from .mixins import RequireAuthMixin


class FoldersViewSet(RequireAuthMixin, ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer