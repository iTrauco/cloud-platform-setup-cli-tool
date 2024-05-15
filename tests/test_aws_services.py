#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner
from src.aws_services_cli import main

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_output(runner):
    result = runner.invoke(main, ['--output', 'test_output.csv'])
    assert result.exit_code == 0
    assert result.output.startswith('Welcome to the Cloud Services CLI!')
    assert 'Output saved to test_output.csv' in result.output

# Add more test cases as needed
