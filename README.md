# silent-speech

Research notes and a first-pass hardware design for a personal **silent-speech wearable**: a device that
recognises words articulated without sound from face/jaw/neck biosignals (sEMG), in the spirit of
AlterEgo and Gaddy's silent-speech work.

> **Not tested in real life.** Nothing in this repository has been built, assembled, worn or validated on a
> real person or in a real lab. Hardware designs have only passed software checks (KiCad ERC/DRC and
> netlist scripts), and software/ML results come from offline datasets or a single dev machine. Treat
> everything as an untested design/research artefact. It is provided **as is, with no warranty**, and is
> **not a medical device** and not safe for use on people without independent engineering and safety review.

## What is here

| Path | What |
|---|---|
| `hw/` | **Current design, rev 0.7**: KiCad project for the sensor pod (nRF/NINA-B4 BLE, ADS1298 AFE), dock, cartridge and electrode/charger tabs; schematics, PCB, BOM, netlists, gerbers + pick-and-place in `hw/fab/`, `hw/SPEC.md` and `hw/pod/design-notes.md` |
| `hw/revisions/` | Earlier snapshots of the same design (schematic, PCB, BOM, notes, gerbers where they existed), named `<date>-<hash>` |
| `research/` | 12 general research tracks (SOTA, modalities, electronics, electrodes, ML pipeline, implants, DIY prior art, ear region, e-tattoos, data, Neuralink, fast personalisation) |
| `research/jaw/` | Focused sweeps: patents, PubMed, OpenBCI forum, BLE link, LCSC parts, tantalum, chip forums, articulation design |
| `scripts/`, `tools/` | Small helper scripts used by the research sweeps |
| `docs/` | Notes from one of the research tracks |

Revision snapshots:
- `hw/revisions/2026-10-07-0d3cfc9e/`
- `hw/revisions/2026-10-07-16618296/`
- `hw/revisions/2026-10-07-392cefe4/`
- `hw/revisions/2026-10-07-7efeed88/`
- `hw/revisions/2026-10-16-01f62380/`
- `hw/revisions/2026-10-16-676691bc/`
- `hw/revisions/2026-10-19-591862ab/`

## 3D models

There are **no custom 3D/CAD models** (no STEP/STL for an enclosure) in this repository: the boards reference
KiCad's stock 3D library only, and the NINA-B4 3D model referenced by the footprint was never generated.
Enclosure design has not been started.

## Notes

- Research files cite sources inline; claims marked "unverified" were not confirmed.
- Third-party datasheets, papers and scraped pages are deliberately **not** included.
- Absolute `/home/...` paths remain in some generated KiCad/router files.

## Licence

Software, scripts and documentation: MIT (`LICENSE`). Hardware design files under `hw/`:
CERN-OHL-P-2.0 (`hw/LICENSE-HARDWARE.txt`).
