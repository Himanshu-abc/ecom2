# context processor
from .models import Tag


def tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}
