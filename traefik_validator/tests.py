from unittest.mock import MagicMock, call

import pytest
from jsonschema.exceptions import ValidationError

from traefik_validator import settings
from traefik_validator.utils import SchemaDownloader, Validator


class TestValidator:

    @pytest.fixture(autouse=True)
    def mock_settings(self):
        settings.STATIC_CONFS_SCHEMA_URL = "https://static.com"
        settings.DYNAMIC_CONFS_SCHEMA_URL = "https://dynamic.com"

    @pytest.fixture(autouse=True)
    def mock_schema_downloader(self, mocker):
        mock_schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "definitions": {
                "httpRouter": {
                    "type": "object",
                    "description": "",
                    "properties": {
                        "rule": {
                            "type": "string",
                            "description": ""
                        },
                    },
                    "additionalProperties": False,
                    "required": [
                        "rule",
                    ]
                },
            },
            "properties": {
                "http": {
                    "type": "object",
                    "properties": {
                        "routers": {
                            "type": "object",
                            "additionalProperties": {
                                "$ref": "#/definitions/httpRouter"
                            }
                        }
                    }
                }
            }
        }
        mocker.patch("traefik_validator.utils.SchemaDownloader.download_from_url", return_value=mock_schema)

    @pytest.fixture(autouse=True)
    def mock_load_yaml(self, mocker):
        mock_yaml = {
            "not_test": 2
        }
        mocker.patch("traefik_validator.utils.Validator.load_yaml", return_value=mock_yaml)

    def test_validator_without_any_files_raise_value_error(self):
        with pytest.raises(ValueError):
            Validator()

    def test_validator_with_both_static_and_dynamic_file_calls_download_twice(
            self,
    ):
        validator = Validator(MagicMock(), MagicMock())
        validator.validate()
        assert SchemaDownloader.download_from_url.call_count == 2
        SchemaDownloader.download_from_url.assert_has_calls(
            [call(url="https://static.com"), call(url="https://dynamic.com")]
        )

    def test_validator_with_static_file_calls_download_one(
            self,
    ):
        validator = Validator(static_conf_file=MagicMock())
        validator.validate()
        assert SchemaDownloader.download_from_url.call_count == 1
        SchemaDownloader.download_from_url.assert_has_calls(
            [call(url="https://static.com")]
        )

    def test_validator_with_dynamic_file_calls_download_one(
            self,
    ):
        validator = Validator(dynamic_conf_file=MagicMock())
        validator.validate()
        assert SchemaDownloader.download_from_url.call_count == 1
        SchemaDownloader.download_from_url.assert_has_calls(
            [call(url="https://dynamic.com")]
        )

    def test_validate_with_invalid_data_raise_error(
            self, mocker
    ):
        mock_yaml = {
            'http': {
                'routers': {
                    'router_test': {
                        'test': ''
                    }
                }
            }
        }
        mocker.patch("traefik_validator.utils.Validator.load_yaml", return_value=mock_yaml)
        validator = Validator(dynamic_conf_file=MagicMock())
        with pytest.raises(ValidationError):
            validator.validate()

    def test_validate_with_valid_data_no_return(
            self, mocker
    ):
        mock_yaml = {
            'http': {
                'routers': {
                    'router_test': {
                        'rule': 'Host(`test.com`) || Host(`www.test.com`)'
                    }
                }
            }
        }
        mocker.patch("traefik_validator.utils.Validator.load_yaml", return_value=mock_yaml)
        validator = Validator(dynamic_conf_file=MagicMock())
        res = validator.validate()
        assert res is None
