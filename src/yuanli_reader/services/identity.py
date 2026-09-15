from __future__ import annotations

from yuanli_reader.domain.models import AdbDeviceRef


def select_device(
    devices: list[AdbDeviceRef],
    enrolled_serial: str | None = None,
) -> AdbDeviceRef:
    if enrolled_serial is not None:
        matches = [device for device in devices if device.serial == enrolled_serial]
        if len(matches) != 1:
            raise RuntimeError("ENROLLED_ADB_DEVICE_NOT_FOUND")
        return matches[0]

    if not devices:
        raise RuntimeError("ADB_DEVICE_NOT_OBSERVED")
    if len(devices) > 1:
        raise RuntimeError("MULTIPLE_ADB_DEVICES")
    return devices[0]
