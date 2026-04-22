# SPDX-FileCopyrightText: 2026 Honeycomb Authors <support@honeycomb.io>
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase

from opentelemetry.util._importlib_metadata import (
    PackageNotFoundError,
    version,
)


class TestDistribution(TestCase):
    def test_package_available(self):
        try:
            version("honeycomb-pycpp-distro")
        except PackageNotFoundError:
            self.fail("honeycomb-pycpp-distro not installed")
