import json
import logging
import re

from cove.views import cove_web_input_error, explore_data_context
from django.conf import settings
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from libcove.lib.converters import convert_spreadsheet
from libcoveoc4ids.common_checks import common_checks_oc4ids
from libcoveoc4ids.config import LibCoveOC4IDSConfig
from libcoveoc4ids.schema import SchemaOC4IDS

logger = logging.getLogger(__name__)


@cove_web_input_error
def explore_oc4ids(request, pk):
    context, db_data, error = explore_data_context(request, pk)
    if error:
        return error

    lib_cove_oc4ids_config = LibCoveOC4IDSConfig(config=settings.COVE_CONFIG)

    upload_dir = db_data.upload_dir()
    upload_url = db_data.upload_url()
    file_name = db_data.original_file.path
    file_type = context["file_type"]

    if file_type == "json":
        # open the data first so we can inspect for record package
        with open(file_name, encoding="utf-8") as fp:
            try:
                json_data = json.load(fp)
            except ValueError as err:
                context = {
                    "sub_title": _("Sorry, we can't process that data"),
                    "link": "index",
                    "link_text": _("Try Again"),
                    "msg": format_html(
                        _(
                            "We think you tried to upload a JSON file, but it is not well formed JSON."
                            '\n\n<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true">'
                            "</span> <strong>Error message:</strong> {}"
                        ),
                        err,
                    ),
                    "error": format(err),
                }
                return render(request, "error.html", context=context)

            if not isinstance(json_data, dict):
                context = {
                    "sub_title": _("Sorry, we can't process that data"),
                    "link": "index",
                    "link_text": _("Try Again"),
                    "msg": _("OC4IDS JSON should have an object as the top level, the JSON you supplied does not."),
                }
                return render(request, "error.html", context=context)

        schema_oc4ids = SchemaOC4IDS(lib_cove_oc4ids_config=lib_cove_oc4ids_config)

        # This feature is disabled, because `flattened.xlsx` was requested once in 14 days as of 2020-10-06.
        # context.update(convert_json(upload_dir, upload_url, file_name, lib_cove_oc4ids_config,
        #                             schema_url=schema_oc4ids.schema_url, replace=True,
        #                             request=request, flatten=True))
    else:
        schema_oc4ids = SchemaOC4IDS(lib_cove_oc4ids_config=lib_cove_oc4ids_config)
        context.update(
            convert_spreadsheet(
                upload_dir,
                upload_url,
                file_name,
                file_type,
                lib_cove_oc4ids_config,
                schema_url=schema_oc4ids.schema_url,
                pkg_schema_url=schema_oc4ids.pkg_schema_url,
            )
        )

        with open(context["converted_path"], encoding="utf-8") as fp:
            json_data = json.load(fp)

    context = common_checks_oc4ids(context, upload_dir, json_data, schema_oc4ids, lib_cove_oc4ids_config)

    for key in ("additional_closed_codelist_values", "additional_open_codelist_values"):
        for path_string, codelist_info in context[key].items():
            if codelist_info["codelist_url"].startswith(schema_oc4ids.codelists):
                codelist_info["codelist_url"] = (
                    "https://standard.open-contracting.org/infrastructure/latest/en/reference/codelists/#"
                    + re.sub(r"([A-Z])", r"\1", codelist_info["codelist"].split(".")[0]).lower()
                )

    if not db_data.rendered:
        db_data.rendered = True
    db_data.save()

    template = "cove_oc4ids/explore.html"

    return render(request, template, context)
