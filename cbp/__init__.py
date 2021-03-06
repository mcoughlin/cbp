#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Michael Coughlin (2013)
#
# This file is part of SeisMon
#
# SeisMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SeisMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SeisMon.  If not, see <http://www.gnu.org/licenses/>

"""Collimated Beam Projector

cbp is for measuring light produced by a laser based source.

.. codeauthor:: Michael Coughlin, Eric Coughlin
"""
from cbp import version

__author__ = 'Michael Coughlin <michael.coughlin@ligo.org>'
__version__ = version.__version__

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
