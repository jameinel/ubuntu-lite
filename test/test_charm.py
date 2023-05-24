# Copyright 2020 Canonical Ltd.
# Licensed under the AGPLv3, see LICENCE file for details.

import os
import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / 'src'))

import charm
from ops import model, testing


testing.SIMULATE_CAN_CONNECT = True


class CharmTestCase(unittest.TestCase):

    def test_on_start(self):
        harness = testing.Harness(charm.Ubuntu)
        harness.begin()
        with patch('charm._get_ubuntu_series', spec=True, return_value='18.04') as lsb_mock:
            with patch('charm.set_application_version', spec=True) as app_version_mock:
                # TODO: This should be harness.emit_start() or something along those lines
                harness.charm.on.start.emit()
                self.assertIsInstance(harness.model.unit.status, model.ActiveStatus)
                # TODO: a way to test the application-version is correct
        self.assertEqual(lsb_mock.call_count, 1)
        self.assertEqual(app_version_mock.call_count, 1)
        self.assertEqual(app_version_mock.call_args, (('18.04',), {}))

    def test_on_update_status(self):
        harness = testing.Harness(charm.Ubuntu)
        harness.begin()
        # TODO: Harness should have a better helper for this
        with patch('os.getloadavg', create=True, return_value=(1.0, 2.2, 3.5)):
            harness.charm.on.update_status.emit()
        status = harness.model.unit.status
        self.assertIsInstance(status, model.ActiveStatus)
        self.assertEqual(status.message, 'load: 1.00 2.20 3.50')

    def test_on_load_action(self):
        self.skipTest("action-get not yet supported by ops.testing.Harness")
        harness = testing.Harness(charm.Ubuntu)
        harness.begin()
        with patch('os.getloadavg', create=True, return_value=(1.1, 2.2, 3.5)):
            # TODO: Harness should have support for triggering actions
            with patch.dict(os.environ, {'JUJU_ACTION_NAME': 'load'}):
                harness.charm.on.load_action.emit()


if __name__ == '__main__':
    unittest.main()
