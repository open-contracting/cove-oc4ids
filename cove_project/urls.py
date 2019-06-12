from django.conf.urls import url
from django.conf.urls.static import static
from django.http import HttpResponseServerError
from django.conf import settings
from django.template import loader
from cove.urls import urlpatterns
import cove_oc4ids.views

urlpatterns += [url(r'^data/(.+)$', cove_oc4ids.views.explore_oc4ids, name='explore')]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler500(request):
    """500 error handler which includes ``request`` in the context.
    """

    context = {
        'request': request,
    }
    context.update(settings.COVE_CONFIG)

    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(context))
