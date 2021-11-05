# Absolute Control

## Introduction

A library for assisting with control of computer processes using python.

Install via pip through PyPi
```bash
pip install absolute-control
```

## Usage

Get all processes running on the system
```python
from absolute_control import get_all_processes

processes = get_all_processes()
```

You may also filter by pid, or by name.
```python
from absolute_control import get_process_by_id, get_process_by_name

pid_processes = get_process_by_id(12345)
name_processes = get_process_by_name('chrome')
```

Kill all processes on the system.
__Note: This will kill all processes on the system, including the ones you have not started provided you have permission to do so.__
```python
from absolute_control import kill_all_processes

kill_all_processes()
```

You may kill processes by name or pid.
```python
from absolute_control import kill_process_by_id, kill_processes_by_name

kill_process_by_id(12345)
kill_processes_by_name('chrome')
```

Start a new process.
```python
from absolute_control import open_process_using_command

process = open_process_using_command('chrome')
```

## Testing

To test the library, run the following commands:

```bash
cd src
python run_tests.py
```

## License

This project is licensed under the MIT license.

## Contribution

This project is open source. You can contribute by making a pull request or by sending an email to [Johnny Irvin](mailto:irvinjohnathan@gmail.com)