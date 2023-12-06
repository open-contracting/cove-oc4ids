import os
import pytest
from cove.input.models import SuppliedData
from django.core.files.base import ContentFile


@pytest.mark.django_db
@pytest.mark.parametrize(
    "json_data",
    [
        # A selection of JSON strings we expect to give a 200 status code, even
        # though some of them aren't valid OC4IDS
        "true",
        "null",
        "1",
        "{}",
    ],
)
def test_explore_page(client, json_data):
    data = SuppliedData.objects.create()
    data.original_file.save("test.json", ContentFile(json_data))
    data.current_app = "cove_oc4ids"
    resp = client.get(data.get_absolute_url())
    assert resp.status_code == 200




@pytest.mark.django_db
def test_codelist_url_extension_codelists(client):
    file_name = os.path.join(
        "tests",
        "fixtures",
        "codelists.json",
    )
    with open(os.path.join(file_name)) as fp:
        user_data = fp.read()
    data = SuppliedData.objects.create()
    data.original_file.save("test.json", ContentFile(user_data))
    data.current_app = "cove_oc4ids"
    resp = client.get(data.get_absolute_url())

    assert resp.status_code == 200
    assert len(resp.context["additional_open_codelist_values"]) == 1
    assert (
        resp.context["additional_open_codelist_values"]["projects/sector"]["codelist_url"]
        == "https://standard.open-contracting.org/infrastructure/latest/en/reference/codelists/#projectsector"
    )
