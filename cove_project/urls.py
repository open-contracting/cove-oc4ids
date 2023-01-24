from cove.urls import handler500  # noqa: F401
from cove.urls import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

import cove_oc4ids.views

urlpatterns += [re_path(r"^data/(.+)$", cove_oc4ids.views.explore_oc4ids, name="explore")]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
