import json

import pytest

from yuanli_reader.adapters.adb import AdbClient
from yuanli_reader.domain.models import DeviceIdentity
from yuanli_reader.services.identity import select_device


def test_rp01_device_identity_is_observed_on_real_reader():
    client = AdbClient()
    devices = client.list_devices()
    if not devices:
        pytest.fail("NOT_OBSERVED: no ADB device is visible")

    if any(device.state == "unauthorized" for device in devices):
        pytest.fail(
            "HUMAN_USB_DEBUG_APPROVAL_REQUIRED: approve the RSA prompt on the reader"
        )

    device = select_device(devices)
    if device.state != "device":
        pytest.fail(f"NOT_OBSERVED: ADB state is {device.state}")

    props = client.get_properties(device.serial)
    identity = DeviceIdentity.from_properties(device.serial, props)
    public = identity.public_dict()
    print("RP01=OBSERVED_ON_REAL_DEVICE")
    print(json.dumps(public, ensure_ascii=False, sort_keys=True))

    assert public["device_id"]
    assert public["model"]
    assert public["android_release"]
