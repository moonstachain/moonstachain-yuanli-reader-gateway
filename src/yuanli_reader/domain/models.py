from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class AdbDeviceRef:
    serial: str
    state: str
    product: str | None = None
    model: str | None = None
    device: str | None = None


@dataclass(frozen=True)
class DeviceIdentity:
    device_id: str
    serial: str
    manufacturer: str
    model: str
    product_name: str
    android_release: str
    sdk: str

    @classmethod
    def from_properties(cls, serial: str, props: dict[str, str]) -> "DeviceIdentity":
        values = {
            "serial": serial.strip(),
            "manufacturer": props.get("ro.product.manufacturer", "").strip(),
            "model": props.get("ro.product.model", "").strip(),
            "product_name": props.get("ro.product.name", "").strip(),
            "android_release": props.get("ro.build.version.release", "").strip(),
            "sdk": props.get("ro.build.version.sdk", "").strip(),
        }
        canonical = json.dumps(
            values,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        device_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return cls(device_id=device_id, **values)

    def public_dict(self) -> dict[str, str]:
        return {
            "device_id": self.device_id,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "product_name": self.product_name,
            "android_release": self.android_release,
            "sdk": self.sdk,
        }
