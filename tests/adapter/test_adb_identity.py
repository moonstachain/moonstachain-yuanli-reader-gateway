import json
from pathlib import Path

import pytest

from yuanli_reader.adapters.adb import AdbClient
from yuanli_reader.domain.models import DeviceIdentity
from yuanli_reader.services.identity import select_device


def _fake_adb(tmp_path: Path) -> tuple[Path, Path]:
    log = tmp_path / "argv.jsonl"
    exe = tmp_path / "adb"
    exe.write_text(
        """#!/usr/bin/env python3
import json, os, sys
with open(os.environ['FAKE_ADB_LOG'], 'a', encoding='utf-8') as f:
    f.write(json.dumps(sys.argv[1:]) + '\\n')
args = sys.argv[1:]
if args == ['devices', '-l']:
    print('List of devices attached')
    print('SER123\\tdevice product:note_air model:Flow device:flow transport_id:1')
elif args == ['-s', 'SER123', 'shell', 'getprop']:
    print('[ro.product.manufacturer]: [ONYX]')
    print('[ro.product.model]: [Flow]')
    print('[ro.product.name]: [flow]')
    print('[ro.build.version.release]: [9]')
    print('[ro.build.version.sdk]: [28]')
else:
    print('unexpected argv', args, file=sys.stderr)
    raise SystemExit(9)
""",
        encoding="utf-8",
    )
    exe.chmod(0o755)
    return exe, log


def test_list_devices_uses_exact_argv_and_parses_ready_device(tmp_path, monkeypatch):
    exe, log = _fake_adb(tmp_path)
    monkeypatch.setenv("FAKE_ADB_LOG", str(log))
    client = AdbClient(adb_path=str(exe))
    devices = client.list_devices()
    assert len(devices) == 1
    assert devices[0].serial == "SER123"
    assert devices[0].state == "device"
    assert devices[0].model == "Flow"
    assert json.loads(log.read_text().splitlines()[0]) == ["devices", "-l"]


def test_get_properties_uses_bounded_getprop_argv(tmp_path, monkeypatch):
    exe, log = _fake_adb(tmp_path)
    monkeypatch.setenv("FAKE_ADB_LOG", str(log))
    client = AdbClient(adb_path=str(exe))
    props = client.get_properties("SER123")
    assert props["ro.product.manufacturer"] == "ONYX"
    assert props["ro.build.version.sdk"] == "28"
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    assert calls[-1] == ["-s", "SER123", "shell", "getprop"]


def test_device_identity_is_stable_and_public_view_redacts_serial():
    props = {
        "ro.product.manufacturer": "ONYX",
        "ro.product.model": "Flow",
        "ro.product.name": "flow",
        "ro.build.version.release": "9",
        "ro.build.version.sdk": "28",
    }
    first = DeviceIdentity.from_properties("SER123", props)
    second = DeviceIdentity.from_properties("SER123", dict(reversed(list(props.items()))))
    assert first.device_id == second.device_id
    assert len(first.device_id) == 64
    public = first.public_dict()
    assert public["model"] == "Flow"
    assert "serial" not in public
    assert "SER123" not in json.dumps(public)


def test_select_device_rejects_multiple_without_enrollment():
    client_devices = [
        type("D", (), {"serial": "A", "state": "device"})(),
        type("D", (), {"serial": "B", "state": "device"})(),
    ]
    with pytest.raises(RuntimeError, match="MULTIPLE_ADB_DEVICES"):
        select_device(client_devices)
