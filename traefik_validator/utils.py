import json
import urllib.request
from io import TextIOWrapper
from typing import Optional, NoReturn

import jsonschema
import yaml

from traefik_validator import settings


class SchemaDownloader:
    """
    A class for downloading schema from https://json.schemastore.org/
    For now, static configs schema is in https://json.schemastore.org/traefik-v2.json
        and dynamic configs schema is in https://json.schemastore.org/traefik-v2-file-provider.json
        which can be found in settings.py.
    """
    def __init__(self):
        self.static_schema_url = settings.STATIC_CONFS_SCHEMA_URL
        self.dynamic_schema_url = settings.DYNAMIC_CONFS_SCHEMA_URL

    @staticmethod
    def download_from_url(url: str) -> dict:
        """ Downloading schema file from given url, return after loading with json """
        with urllib.request.urlopen(url) as f:
            schema = json.loads(f.read().decode('utf-8'))

        return schema

    def get_static_schema(self) -> dict:
        return self.download_from_url(url=self.static_schema_url)

    def get_dynamic_schema(self) -> dict:
        return self.download_from_url(url=self.dynamic_schema_url)


class Validator:
    """
    Validating user yaml file with traefik schema.
    User should at least pass either a dynamic config file or a static config file.
    """
    def __init__(
            self,
            static_conf_file: Optional[TextIOWrapper] = None,
            dynamic_conf_file: Optional[TextIOWrapper] = None
    ):
        if not any([static_conf_file, dynamic_conf_file]):
            raise ValueError("Use should pass either static config file or dynamic config file")

        self.static_conf_file = static_conf_file
        self.dynamic_conf_file = dynamic_conf_file

        self.schema_downloader = SchemaDownloader()

    def validate(self) -> NoReturn:
        """ An interface to call validators """
        self._validate_static()
        self._validate_dynamic()

    def _validate_static(self) -> NoReturn:
        """ Validate static config file, if it has been provided by user. """
        if not self.static_conf_file:
            return

        schema_file = self.schema_downloader.get_static_schema()
        config_file = self.load_yaml(self.static_conf_file)
        jsonschema.validate(instance=config_file, schema=schema_file)

    def _validate_dynamic(self) -> NoReturn:
        """ Validate dynamic config file, if it has been provided by user. """
        if not self.dynamic_conf_file:
            return

        schema_file = self.schema_downloader.get_dynamic_schema()
        config_file = self.load_yaml(self.dynamic_conf_file)
        jsonschema.validate(instance=config_file, schema=schema_file)

    @staticmethod
    def load_yaml(file: TextIOWrapper) -> dict:
        return yaml.load(file, Loader=yaml.FullLoader)
