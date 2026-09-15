from __future__ import annotations

import re
import subprocess

from yuanli_reader.domain.models import AdbDeviceRef

_GETPROP_RE = re.compile(r"^\[([^]]+)\]: \[(.*)\]$")


class AdbClient:
    def __init__(self, adb_path: str = "adb", timeout: float = 10.0):
        self.adb_path = adb_path
        self.timeout = timeout

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self.adb_path, *args],
            shell=False,
            capture_output=True,
            text=True,
            timeout=self.timeout,
            check=True,
        )

    def list_devices(self) -> list[AdbDeviceRef]:
        result = self._run(["devices", "-l"])
        devices: list[AdbDeviceRef] = []
        for raw in result.stdout.splitlines():
            line = raw.strip()
            if not line or line.startswith("List of devices attached"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            serial, state = parts[0], parts[1]
            metadata: dict[str, str] = {}
            for token in parts[2:]:
                if ":" in token:
                    key, value = token.split(":", 1)
                    metadata[key] = value
            devices.append(
                AdbDeviceRef(
                    serial=serial,
                    state=state,
                    product=metadata.get("product"),
                    model=metadata.get("model"),
                    device=metadata.get("device"),
                )
            )
        return devices

    def get_properties(self, serial: str) -> dict[str, str]:
        result = self._run(["-s", serial, "shell", "getprop"])
        props: dict[str, str] = {}
        for line in result.stdout.splitlines():
            match = _GETPROP_RE.match(line.strip())
            if match:
                props[match.group(1)] = match.group(2)
        return props
