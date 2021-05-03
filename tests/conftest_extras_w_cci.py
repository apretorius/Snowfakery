from unittest.mock import patch

import pytest
from pytest import fixture

from cumulusci.tests.pytest_plugins.pytest_sf_vcr import (
    vcr_config as cci_vcr_config,
    salesforce_vcr,
)

from cumulusci.tests.util import DummyOrgConfig

DUMMY_ORGNAME = "pytest_sf_orgconnect_dummy_orgconfig"


@pytest.fixture(scope="session")
def fallback_org_config():
    def fallback_org_config():
        return DummyOrgConfig(
            {
                "instance_url": "https://orgname.my.salesforce.com",
                "access_token": "pytest_sf_orgconnect_abc123",
                "id": "ORGID/ORGID",
            },
            DUMMY_ORGNAME,
        )

    original_get_org = None

    def get_org(self, name: str):
        if name == DUMMY_ORGNAME:
            return DUMMY_ORGNAME, fallback_org_config()
        else:
            return original_get_org(self, name)

    p = patch(
        "cumulusci.cli.runtime.CliRuntime.get_org",
        get_org,
    )
    original_get_org = p.get_original()[0]
    with p:
        yield fallback_org_config


vcr_config = fixture(cci_vcr_config, scope="module")
vcr = fixture(salesforce_vcr, scope="module")


__all__ = ["vcr_config", "vcr", "fallback_org_config"]