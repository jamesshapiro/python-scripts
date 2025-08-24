# extract_repo.py
# Usage: python extract_repo.py
# Output: extracted_repo.txt (in the current working directory / repo root)

import os
import sys
import fnmatch
from pathlib import Path

REPO_ROOT = Path.cwd()
OUTPUT_FILE = REPO_ROOT / "extracted_repo.txt"

# --- Tunables ---
MAX_FILE_SIZE = 800_000  # ~0.8 MB

DEFAULT_IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".DS_Store", "__pycache__", ".venv", "venv", "env",
    "node_modules", "bower_components", ".pnpm-store", ".yarn", ".yarn/cache",
    ".vscode", ".idea", ".terraform", ".terragrunt-cache", ".next", ".nuxt", ".expo",
    "dist", "build", "out", "coverage", "target", "Pods", "Carthage", "DerivedData",
    ".pytest_cache", ".mypy_cache", ".gradle", ".cache", ".parcel-cache",
    "src/hooks", "src/components/ShiftBy",
}

INCLUDE_EXTS = {
    ".py", ".pyi", ".ipynb", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".java", ".kt", ".kts", ".swift", ".rb", ".go", ".rs",
    ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh",
    ".cs", ".scala", ".m", ".mm", ".pl", ".pm", ".lua", ".php", ".r", ".jl",
    ".sh", ".bash", ".zsh", ".ps1", ".cmd", ".bat", ".fish", ".awk",
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini", ".conf", ".cfg", ".hcl",
    ".tf", ".tfvars", ".tfstate", ".tfplan",
    ".env.example", ".dockerignore", ".editorconfig",
    ".md", ".rst", ".tex", ".graphql", ".gql",
    ".gradle", ".gradle.kts", ".properties",
    ".make", ".mk", ".bazel", ".bzl", ".WORKSPACE", ".buck", ".nix",
}

INCLUDE_SPECIAL = {
    "Dockerfile", "Makefile", "Makefile.win", "CMakeLists.txt", "Procfile",
    "Gemfile", "Rakefile", "BUILD", "WORKSPACE", "Justfile"
}

EXCLUDE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".ico", ".icns", ".webp",
    ".ai", ".psd", ".sketch", ".fig",
    ".mp3", ".wav", ".flac", ".m4a", ".ogg", ".mp4", ".mkv", ".mov", ".avi", ".webm",
    ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar", ".jar",
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".key",
    ".o", ".a", ".so", ".dylib", ".dll", ".bin", ".exe", ".class", ".pyc", ".pyo",
    ".wasm",
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "Pipfile.lock",
}

EXCLUDE_FILES = {
    ".terraform.lock.hcl",
    ".eslintrc.json",
    "src/components/ShiftBy/ShiftBy.js",
    "src/components/ShiftBy/index.js",
    "package-build-snippet.json",
    "LICENSE",
    "src/reset.css",
    "src/styles.css",
    ".gitignore",
    "dotgit--hooks--pre-push"
}

def read_gitignore_patterns(root):
    patterns = []
    gi = root / ".gitignore"
    if gi.exists():
        for line in gi.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.endswith("/"):
                patterns.append(f"**/{line.rstrip('/')}/**")
            else:
                patterns.append(line)
    return patterns

def path_matches_any(path, patterns):
    rel = path.as_posix()
    for pat in patterns:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel, f"**/{pat}"):
            return True
    return False

def should_ignore_dir(rel_dir, gitignore_patterns):
    name = rel_dir.name
    full_path = rel_dir.as_posix()
    
    print(f"🔍 Checking directory: {full_path} (name: {name})")
    
    # Check if the full path matches any of the ignored directories
    if full_path in DEFAULT_IGNORED_DIRS:
        print(f"  ✅ Excluded by DEFAULT_IGNORED_DIRS (full path): {full_path}")
        return True
    
    # Check if just the directory name matches (for backward compatibility)
    if name in DEFAULT_IGNORED_DIRS:
        print(f"  ✅ Excluded by DEFAULT_IGNORED_DIRS (name only): {name}")
        return True
    
    if path_matches_any(rel_dir, gitignore_patterns):
        print(f"  ✅ Excluded by gitignore patterns: {name}")
        return True
    
    print(f"  ❌ Not excluded: {name}")
    return False

def is_included_file(path, gitignore_patterns):
    rel = path.relative_to(REPO_ROOT)
    name = path.name

    if path_matches_any(rel, gitignore_patterns):
        return False

    # Check if file is in the exclude list
    if name in EXCLUDE_FILES:
        return False

    lower_name = name.lower()
    ext = path.suffix

    if lower_name in {n.lower() for n in EXCLUDE_EXTS if not n.startswith(".")}:
        return False
    if ext.lower() in EXCLUDE_EXTS:
        return False

    if name in INCLUDE_SPECIAL:
        pass
    else:
        if ext and ext not in INCLUDE_EXTS:
            if name.startswith(".") and ext == "":
                pass
            else:
                return False

    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return False
    except OSError:
        return False

    try:
        with path.open("rb") as f:
            chunk = f.read(4096)
            if b"\x00" in chunk:
                return False
    except Exception:
        return False

    return True

def build_tree(included_files):
    root = {}
    for p in included_files:
        parts = p.parts
        node = root
        for i, part in enumerate(parts):
            is_file = (i == len(parts) - 1)
            node = node.setdefault(part, {} if not is_file else None)
    lines = []
    def render(node, prefix=""):
        entries = sorted(node.items(), key=lambda kv: (kv[1] is None, kv[0].lower()))
        total = len(entries)
        for i, (name, child) in enumerate(entries):
            is_last = (i == total - 1)
            branch = "└── " if is_last else "├── "
            lines.append(prefix + branch + name)
            if child is not None:
                extension = "    " if is_last else "│   "
                render(child, prefix + extension)
    render(root)
    return "\n".join(lines)

def write_output(tree_text, files):
    with OUTPUT_FILE.open("w", encoding="utf-8", errors="replace") as out:
        out.write("# Repository Code Legend\n\n")
        out.write("```\n")
        out.write(tree_text)
        out.write("\n```\n\n")
        out.write("# Extracted Code\n\n")
        for rel_path in files:
            full_path = REPO_ROOT / rel_path
            try:
                text = full_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            out.write("```\n")
            out.write(str(rel_path).replace("\\", "/"))
            out.write("\n\n")
            out.write(text.rstrip("\n"))
            out.write("\n```\n\n")

def main():
    gitignore_patterns = read_gitignore_patterns(REPO_ROOT)
    included = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirpath = Path(dirpath)
        rel_dir = dirpath.relative_to(REPO_ROOT)
        to_remove = []
        for d in dirnames:
            d_rel = (rel_dir / d)
            if should_ignore_dir(d_rel, gitignore_patterns):
                to_remove.append(d)
        for d in to_remove:
            try:
                dirnames.remove(d)
            except ValueError:
                pass
        for f in filenames:
            full = dirpath / f
            if full.resolve() == OUTPUT_FILE.resolve() or full.name == Path(__file__).name:
                continue
            rel = full.relative_to(REPO_ROOT)
            if is_included_file(full, gitignore_patterns):
                included.append(rel)
    included = sorted(included, key=lambda p: p.as_posix().lower())
    tree_text = build_tree(included)
    write_output(tree_text, included)
    print(f"Wrote {len(included)} files to {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
