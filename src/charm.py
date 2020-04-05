#!/usr/bin/env python3

import os
import subprocess

from ops import charm, main, model


def set_application_version(version):
    # TODO: application-version-set should be modeled in the framework
    subprocess.check_call(['application-version-set', self._get_ubuntu_series()])


def _get_ubuntu_series(self):
    with open('/etc/lsb-release', 'rt') as lsb:
        for line in lsb:
            line = line.strip()
            if line.startswith('DISTRIB_RELEASE='):
                series = line.split('=', 1)[1]
                return series
    return '<unknown>'


class Ubuntu(charm.CharmBase):
    """The simplest of charms that just gets Ubuntu up and running.
    """

    def __init__(self, framework, key):
        super().__init__(framework, key)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.update_status, self._on_update_status)

    def _on_start(self, event):
        self.model.unit.status = model.ActiveStatus()
        set_application_version(_get_ubuntu_series())

    def _on_update_status(self, event):
        load1min, load5min, load15min = os.getloadavg()
        self.model.unit.status = model.ActiveStatus(
            'load: {:.2f} {:.2f} {:.2f}'.format(load1min, load5min, load15min))


if __name__ == '__main__':
    main.main(Ubuntu)
