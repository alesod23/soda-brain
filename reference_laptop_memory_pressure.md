---
name: reference_laptop_memory_pressure
description: Laptop has 16 GB but Windows sees only 11.7 GB - 4 GB is the Radeon 760M UMA carve-out, not a VM.
metadata:
  type: reference
---

ThinkPad P14s Gen 5 AMD (21ME002SFR), Ryzen 5 PRO 8640HS + Radeon 760M,
BIOS R2LET40W 1.21. **16 GB installed as ONE Samsung DDR5-5600 SODIMM, slot 1 of
2 - the second slot is free, array max 64 GB.** Running single-channel.

Windows sees **11.667 GB**. The missing 4.33 GB is "Hardware reserved" =
the iGPU UMA frame buffer (registry
`HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000`
`HardwareInformation.qwMemorySize` = exactly 4.00 GB) plus ~330 MB firmware/ACPI.

**It is NOT WSL, Hyper-V or a VM** - do not re-diagnose it that way. VM memory
shows as "In use", never "Hardware reserved", which is a pre-boot firmware
carve-out. (`VirtualMachinePlatform` is enabled, `HypervisorPlatform` disabled,
VBS/HVCI on but `Secure System` is only ~180 MB and comes out of visible RAM.)

The real day-to-day pressure is commit, not the carve-out: 8 simultaneous Claude
Code sessions each spawn a full MCP stack. See
[[feedback_mcp_per_session_not_global]]. Diagnose with committed-vs-limit
(`\Memory\Committed Bytes` / `Commit Limit`), not with "in use" - at >90% of the
limit Windows trims every working set hard and the machine thrashes with
processes sitting at ~0 working set.
