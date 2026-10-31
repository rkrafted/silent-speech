# Rev 0.7 plan (decided 2026-10-16, BUILT 2026-10-16; what was built is in hw/SPEC.md and design-notes §2d)

State before this: rev 0.6 is DONE and clean. Pod DRC 0 / unconnected 0 / ERC 0 / 123 net rules. It has the
swappable battery cartridge, the electrode tab inside the outline, and order files for pod, tab_electrode,
tab_charger and cartridge. Review zip sha256 1c54b19a…0436, in both NDA annexes. Rev 0.4 backup:
/tmp/claude-1000/-home-neo/5c4f22cc-9353-4aa5-ba80-e503a66675b9/scratchpad/backup-rev04 (temporary).

## Owner decisions
1. **Remove USB charging from the pod.** Batteries are charged only outside the pod, in a charging dock.
2. **Two pods worn at the same time, sampling in sync** (16 channels). This must work in hardware.
3. Put a **fuel gauge** in the freed space, and try to **shrink the board**. "As small as possible"; never upsize
   without asking.

## Pod changes
- **Remove:** U5 MCP73831, R11 (PROG), C28 (VBUS 10u), D5 SMAJ5.0A, R16 (VBUS -> VBUS_MOD) and the VBUS net.
  - NINA pin 31 (VBUS): check UBX-17052099 for the rule when USB is unused (likely leave open or tie per the manual).
  - Keep C29 (+BATT bulk) and Q2 (reverse-polarity FET).
  - Firmware: there is no USBDETECTED any more; charging state comes only from the dock.
- **Two-pod sync:**
  - ADS1298 CLKSEL is now hard-wired to DVDD (internal clock), so a pod can NOT take an external clock. Move CLKSEL
    to a NINA GPIO with a 100k pull-up (default = internal clock). Use a GPIO that is NOT near the radio; EXP1-5
    are near the radio, but a static signal is fine there.
  - The master outputs CLK (CONFIG1 CLK_EN); the slave sets CLKSEL low and takes CLK in.
  - Freed pogo pins: P11 (was VBUS) -> CLK_SYNC. P12 stays GND (the link needs a shared ground).
  - START sync: either one more pin, or both pods start by command and firmware corrects the fixed sample offset.
    Pick one, and write down why.
  - TP1 (CLK) and TP2 (START) now sit under the cartridge. Fine once CLK/START are on the pogo grid.
- **Fuel gauge MAX17048** (tiny package):
  - VDD and CELL on the battery side (+BATT);
  - I2C on two NINA GPIOs that are NOT near the radio (I2C must not use EXP1-5);
  - pull-ups 4.7k-10k to +3V3;
  - ALRT optional.
- **Shrink:** after removal, try 24 x 28 (keep the NINA antenna rules and the cartridge strip). Re-run the full
  build: build.sh; route_tab.py for the tab; fix_gnd_pin is conditional.
- Update `check_nets.py` rules: no VBUS rules, plus CLKSEL / CLK_SYNC / fuel-gauge rules.

## Other boards
- **Charger tab:** delete (drop it from fab.py BOARDS / TAB_BOM, from the review package and from the 3D page).
- **Electrode tab:** carries CLK_SYNC + GND as well, so the two pods can be linked with a short lead. Grid contacts
  P1-P10 + P11 (CLK) + P12 (GND): a 2x6 SMD header, or 2x5 plus a 2-pin link header. Re-run route_tab.py, which
  needs F.Cu-only planar routing.
- **New charging dock board** (`gen_dock.py`):
  - USB-C (5.1k CC pull-downs) -> TVS -> MCP73831.
  - R_PROG for the 402020 cell, about 0.5 C = 60 mA: 15k gives about 67 mA.
  - Two pads laid out exactly like the pod's TP15/TP16 (pod_geom.CART_PADS), so the cartridge's spring pins land on
    the dock the same way they land on the pod.
  - The dock holds one cartridge. Mechanical clip with the case.
  - No LEDs on the pod; the dock MAY have a charge LED (it is not worn). Ask the owner.

## Checks
- **EU common-charger rule 2022/2380:** does it apply to the dock or to the pod? [verify]
- **LCSC numbers still open** (queue item ss-lcsc-parts): tall pogo, 2x5 (or 2x6) SMD header, BLM15HD182SN1D,
  W25Q128JVPIQ. Add MAX17048 to that search.

## Docs to update after
- design-notes.md (rev 0.7 section);
- review README: remove question 6 (charger power path), add sync + dock questions;
- rezip the review package, then update the NDA annex sha256;
- 3D page (artifact 6sZ9LUmYEDawdA3K9jdUz9): no charger tab, add the dock, update the costs;
- research/jaw/readiness.md.
