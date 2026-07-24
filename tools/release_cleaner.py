#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, zipfile
REMOVE_DIRS={".pytest_cache","__pycache__",".mypy_cache",".ruff_cache","htmlcov"}
REMOVE_FILES={".coverage",".DS_Store","Thumbs.db"}
def clean(root: Path):
    for p in sorted(root.rglob("*"), reverse=True):
        if p.is_dir() and p.name in REMOVE_DIRS: shutil.rmtree(p, ignore_errors=True)
        elif p.is_file() and (p.name in REMOVE_FILES or p.suffix in {".pyc",".pyo"}): p.unlink(missing_ok=True)
def build(root: Path, output: Path):
    clean(root)
    with zipfile.ZipFile(output,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(root.parent))
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("root",type=Path); ap.add_argument("output",type=Path,nargs="?"); a=ap.parse_args(); clean(a.root)
    if a.output: build(a.root,a.output)
