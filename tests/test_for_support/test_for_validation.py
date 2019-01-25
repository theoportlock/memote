# -*- coding: utf-8 -*-

# Copyright 2019 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Ensure the expected functioning of ``memote.support.validation``."""

from __future__ import absolute_import

import os
import pytest

import memote.support.validation as val

my_path = os.path.abspath(os.path.dirname(__file__))
sbml_valid  = os.path.join(my_path, "data/validation/tiny_FBC.xml")
sbml_invalid = os.path.join(my_path, "data/validation/tiny_FBC2.xml")


@pytest.mark.parametrize("filename, expected", [
    (sbml_valid, [0, 1, False]),
    (sbml_invalid, [1, 0, True])])
def test_run_cobrapy_validation(filename, expected):
    notifications = {"warnings": [], "errors": []}
    model, _ = val.run_cobrapy_validation(filename, notifications)
    assert len(notifications["errors"]) == expected[0]
    assert len(notifications["warnings"]) == expected[1];
    assert (model is None) == expected[2]


@pytest.mark.parametrize("filename, expected", [
    (sbml_valid, [0, 0]),
    (sbml_invalid, [1, 0])])
def test_run_libsbml_validation(filename, expected):
    notifications = {"warnings": [], "errors": []}
    val.run_libsbml_validation(filename, notifications)
    assert len(notifications["errors"]) == expected[0]
    assert len(notifications["warnings"]) == expected[1];