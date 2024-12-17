# Copyright 2020 Canonical Ltd.
# Licensed under the AGPLv3, see LICENCE file for details.

import pathlib
import sys
import unittest
from unittest.mock import patch

# TODO (jam): 2024-12-17 Find a way to remove this
sys.path.insert(0, str(pathlib.Path(__file__).parents[1] / 'src'))

import charm
from ops import testing


def test_start_calls_load():
    """Test that the charm responds to a start event by checking the load on the system."""
    ctx = testing.Context(charm.Ubuntu)
    state = testing.State(leader=True)
    with patch('charm._get_ubuntu_series', spec=True, return_value='18.04') as lsb_mock:
        out = ctx.run(ctx.on.start(), state)
        assert out.workload_version == '18.04'
        assert lsb_mock.call_count == 1
        # the workload_version_history only holds the previous values, but this
        # ensures that we aren't calling the update multiple times
        assert ctx.workload_version_history == []

def test_update_status():
    """Test that the status message reflects the result from load."""
    ctx = testing.Context(charm.Ubuntu)
    state = testing.State(leader=True)
    with patch('os.getloadavg', create=True, return_value=(1.0, 2.2, 3.5)):
        out = ctx.run(ctx.on.update_status(), state)
        assert out.unit_status == testing.ActiveStatus('load: 1.00 2.20 3.50')

def test_on_load_action():
    """Test that you can call the `load` action and it returns appropriate content."""
    ctx = testing.Context(charm.Ubuntu)
    state = testing.State(leader=True)
    with patch('os.getloadavg', create=True, return_value=(1.1, 2.2, 3.5)):
        out = ctx.run(ctx.on.action("load"), state)
        _ = out
        assert ctx.action_results == {'15min': 3.5, '1min': 1.1, '5min': 2.2}


if __name__ == '__main__':
    unittest.main()
