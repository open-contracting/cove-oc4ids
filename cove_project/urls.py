from django.conf import settings
from django.conf.urls import include, re_path
from django.conf.urls.static import static
from django.http import HttpResponseServerError
from django.template import loader
from django.views.generic import RedirectView

from cove_oc4ids.views import explore_oc4ids

urlpatterns = [
    # Allow cove to respond on both the root url and a prefixed
    # one
    re_path(r'^$', RedirectView.as_view(pattern_name='index',
                                        permanent=False)),

    re_path(settings.URL_PREFIX, include('cove.urls')),
    re_path(settings.URL_PREFIX + 'data/(.+)$', explore_oc4ids,
            name='explore'),
]

# Add static media urls so that the inbuilt dev server can serve them
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
