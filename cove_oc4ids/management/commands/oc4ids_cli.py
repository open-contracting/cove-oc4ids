import json
import os
import sys

from cove.management.commands.base_command import CoveBaseCommand, SetEncoder
from django.conf import settings
from django.core.management.base import CommandError
from libcoveoc4ids.api import APIException, oc4ids_json_output


class Command(CoveBaseCommand):
    help = "Run Command Line version of Cove OC4IDS"

    def handle(self, file, *args, **options):
        super(Command, self).handle(file, *args, **options)

        try:
            result = oc4ids_json_output(
                self.output_dir, file
            )
        except APIException as e:
            self.stdout.write(str(e))
            sys.exit(1)

        with open(os.path.join(self.output_dir, "results.json"), "w+") as result_file:
            json.dump(result, result_file, indent=2, sort_keys=True, cls=SetEncoder)
