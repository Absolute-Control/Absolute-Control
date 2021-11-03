# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from typing import Any
from unittest.mock import Mock, patch

from psutil import AccessDenied
from pytest import fixture, mark
from absolute_control import (get_all_processes, get_process_by_id, get_processes_by_name,
                 kill_all_processes, kill_process_by_id,
                 kill_processes_by_name, open_process_using_command)
from absolute_control.models.process import Model


@fixture
def fake_util_process() -> 'psutil.Process':
    mock_process = Mock(pid = 1)
    mock_process.name.return_value = 'foo'
    mock_process.cmdline.return_value = ['/usr/bin/foo', 'bar']
    mock_process.status.return_value = 'running'
    mock_process.username.return_value = 'root'
    mock_process.cpu_percent.return_value = 1
    mock_process.memory_percent.return_value = 1
    mock_process.kill.return_value = Mock()

    return mock_process

def test_model_from_process(fake_util_process):
    model = Model.from_process(fake_util_process)

    assert model.pid == 1
    assert model.name == 'foo'
    assert model.cmdline == ['/usr/bin/foo', 'bar']
    assert model.status == 'running'
    assert model.username == 'root'
    assert model.cpu_percent == 1
    assert model.memory_percent == 1

@mark.parametrize('attribute, value', [
    ('name', 'foo'),
    ('cmdline', ['/usr/bin/foo', 'bar']),
    ('status', 'running'),
    ('username', 'root'),
    ('cpu_percent', 1),
    ('memory_percent', 1),
])
def test_get_all_processes(fake_util_process: Model, attribute: str, value: Any):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        processes = get_all_processes()

        assert len(processes) == 1
        assert getattr(processes[0], attribute) == value

@mark.parametrize('attribute, value', [
    ('name', 'foo'),
    ('cmdline', ['/usr/bin/foo', 'bar']),
    ('status', 'running'),
    ('username', 'root'),
    ('cpu_percent', 1),
    ('memory_percent', 1),
])
def test_get_process_by_id(fake_util_process: Model, attribute: str, value: Any):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        process = get_process_by_id(1)

        assert getattr(process, attribute) == value

def test_get_process_by_id_no_match(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        process = get_process_by_id(2)

        assert process is None

def test_get_processes_by_name(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        processes = get_processes_by_name('foo')

        assert len(processes) == 1
        assert processes[0].name == 'foo'

def test_get_processes_by_name_no_match():
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[]
    ):
        processes = get_processes_by_name('foo')

        assert len(processes) == 0

def test_kill_all_processes(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_all_processes()
        
        assert fake_util_process.kill.called

def test_kill_process_by_id(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_process_by_id(1)

        assert fake_util_process.kill.called

def test_kill_process_by_id_no_match(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_process_by_id(2)

        assert not fake_util_process.kill.called

def test_kill_processes_by_name(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_processes_by_name('foo')

        assert fake_util_process.kill.called

def test_kill_processes_by_name_no_match(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_processes_by_name('bar')

        assert not fake_util_process.kill.called

def test_open_process_using_command(fake_util_process: Model):
    with patch(
        'absolute_control.infrastructure.process.Popen',
        return_value=fake_util_process
    ):
        process = open_process_using_command('foo')

        assert Model.from_process(fake_util_process) == process

def test_kill_all_processes_raises_access_denied(fake_util_process: Model):
    fake_util_process.kill.side_effect = AccessDenied
    with patch(
        'absolute_control.infrastructure.process.process_iter',
        return_value=[fake_util_process]
    ):
        kill_all_processes()

        fake_util_process.kill.called_once()
