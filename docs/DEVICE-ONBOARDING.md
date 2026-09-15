# Device Onboarding｜YOS-READER0 G0

## Trust boundary

The first enrollment is USB/ADB only. No root, bootloader unlock, firmware flash, DRM bypass, or unrestricted shell is required.

## Human steps on the reader

1. Unlock the reader and keep the screen awake.
2. Open system settings.
3. Enable the reader's USB debugging / Android debugging option.
4. Reconnect the USB cable if the setting requests it.
5. If an RSA fingerprint dialog appears, review it and tap **Allow / 允许** on the reader.
6. Do not enable any root, OEM unlocking, or firmware options.

Community-documented Dedao reader builds commonly place USB debugging under a path similar to `设置 → 通用设置 → 应用设置 → USB调试模式`; exact wording can vary by model/firmware.

## Mac verification

Run:

```bash
adb devices -l
```

Expected state progression:

- no row: `NOT_OBSERVED`; check data-capable cable, USB mode, and USB debugging;
- `unauthorized`: `HUMAN_USB_DEBUG_APPROVAL_REQUIRED`; approve on reader;
- `device`: ready for RP-01 identity enrollment.

Raw ADB serials are runtime-only. Committed evidence uses a SHA-256-derived `device_id` and sanitized device properties.
