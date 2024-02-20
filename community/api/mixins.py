from django.shortcuts import get_object_or_404
from community.models import Blog

class MutlipleFieldMixin:
    """
    Mixin to filter comments based on pk and id
    """
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        post_pk = Blog.objects.get(pk=self.kwargs['pk']).id
        filter["post"] = post_pk
        filter["id"] = self.kwargs["id"]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj