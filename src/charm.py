#!/usr/bin/env python3
# Copyright 2020 Canonical Ltd.
# Licensed under the AGPLv3, see LICENCE file for details.

import os
import logging
import subprocess

from ops import (
    charm,
    main,
    model,
)


logger = logging.getLogger("ubuntu-lite")


def set_application_version(version):
    # TODO: application-version-set should be modeled in the framework
    subprocess.check_call(['application-version-set', version])


def _get_ubuntu_series():
    """Read /etc/lsb-release to get the Ubuntu release number."""
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

    def __init__(self, framework, *args):
        super().__init__(framework, *args)

        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self.framework.observe(self.on.load_action, self._on_load_action)

        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.secret_changed, self._on_secret_changed)

    def _on_start(self, event):
        self.model.unit.status = model.ActiveStatus()
        set_application_version(_get_ubuntu_series())

    def _on_update_status(self, event):
        load1min, load5min, load15min = os.getloadavg()
        self.model.unit.status = model.ActiveStatus(
            'load: {:.2f} {:.2f} {:.2f}'.format(load1min, load5min, load15min))

    def _on_load_action(self, event):
        load1min, load5min, load15min = os.getloadavg()
        event.set_results({
            "1min": load1min,
            "5min": load5min,
            "15min": load15min,
        })

    def _on_config_changed(self, event):
        logger.info("config: %r", dict(self.config))
        mysec = self.config.get('mysec')
        if mysec:
            sec = self.model.get_secret(id=mysec, label="mysec")
            content = sec.get_content()
            peek = sec.peek_content()
            logger.info("secret, I shouldn't be telling you this: %r", content)
            logger.info("secret, peeking ahead: %r", peek)

    def _on_secret_changed(self, event):
        logger.info("secret event: %r", event)
        content = event.secret.get_content()
        peek = event.secret.peek_content()
        logger.info("secret, I shouldn't be telling you this: %r", content)
        logger.info("secret, peeking ahead: %r", peek)


if __name__ == '__main__':
    main.main(Ubuntu)
