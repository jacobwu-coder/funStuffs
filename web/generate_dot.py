"""generate_dot.py - render .dot files to plots/ (SVG/PNG)
"""
from pathlib import Path
import subprocess
import sys

def render_dot(dot_path: Path, out_dir: Path, formats=("svg",)):
    out_dir.mkdir(parents=True, exist_ok=True)
    basename = dot_path.stem
    results = {}
    for fmt in formats:
        out_file = out_dir / f"{basename}.{fmt}"
        try:
            subprocess.run(["dot", f"-T{fmt}", str(dot_path), "-o", str(out_file)], check=True)
            results[fmt] = str(out_file)
        except Exception:
            results[fmt] = None
    return results


def find_dot_files(src_dir: Path):
    return sorted(src_dir.glob("**/*.dot"))


def main():
    src = Path('web/dots')
    out = Path('plots')
    formats=("svg","png")
    if not src.exists():
        print('no src dir', src)
        sys.exit(2)
    dots = find_dot_files(src)
    if not dots:
        print('no .dot files')
        return
    for d in dots:
        res=render_dot(d,out,formats)
        print(d.name, res)

if __name__=='__main__':
    main()
