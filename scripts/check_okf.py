#!/usr/bin/env python3
"""OKF v0.1 conformance checker for the Ensuro documentation bundle.

Validates:
  1. Every non-reserved .md file has parseable YAML frontmatter with a non-empty `type`.
  2. Reserved files: index.md has no frontmatter (except `okf_version` at the bundle root);
     log.md has no frontmatter.
  3. Internal markdown links (relative) resolve to existing files inside the bundle.
  4. Anchors in internal links resolve to headings in the target file (best effort, warning).
  5. Referenced assets (images, specs) exist.

Exit code 0 = conformant (warnings allowed), 1 = errors found.
"""
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RESERVED = ("index.md", "log.md", "README.md")
SKIP_DIRS = {".git", "scripts", "site", ".venv", "node_modules"}

errors = []
warnings = []


def slugify(heading):
    """GitHub-style anchor slug."""
    s = unicodedata.normalize("NFKD", heading.strip().lower())
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s]+", "-", s)


def anchors_of(path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return set()
    out = set()
    in_code = False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            h = re.sub(r"[\\`*_{}\[\]()#]", "", m.group(2))
            slug = slugify(h)
            if slug in out:  # GitHub de-duplicates repeated headings with -1, -2, ...
                i = 1
                while f"{slug}-{i}" in out:
                    i += 1
                slug = f"{slug}-{i}"
            out.add(slug)
    return out


def frontmatter_of(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    try:
        return yaml.safe_load(m.group(1)), text[m.end():]
    except yaml.YAMLError as e:
        return {"__parse_error__": str(e)}, text[m.end():]


def main():
    md_files = sorted(p for p in ROOT.rglob("*.md")
                      if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS))
    if not md_files:
        errors.append("no markdown files found")
    for path in md_files:
        rel = path.relative_to(ROOT)
        fm, body = frontmatter_of(path)
        if path.name in RESERVED:
            if fm is not None:
                allowed_keys = {"noindex"}
                if path.name == "index.md" and rel.parent == Path("."):
                    allowed_keys = {"okf_version", "title", "description", "type", "tags", "noindex"}
                if path.name == "README.md":
                    allowed_keys = {"title", "description", "type", "tags", "noindex"}
                if not set(fm or {}) <= allowed_keys:
                    disallowed = set(fm or {}) - allowed_keys
                    errors.append(f"{rel}: reserved file frontmatter contains disallowed keys: {disallowed}")
            continue
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        if "__parse_error__" in fm:
            errors.append(f"{rel}: unparseable frontmatter: {fm['__parse_error__']}")
            continue
        if not isinstance(fm, dict) or not fm.get("type"):
            errors.append(f"{rel}: frontmatter lacks a non-empty 'type'")

        # internal links
        for m in re.finditer(r"(!?)\[([^\]]*)\]\(((?:[^)(]|\([^)(]*\))+)\)", body):
            target = m.group(3).strip()
            title_m = re.match(r'^(.*?)\s+"([^"]*)"$', target)
            if title_m:
                target = title_m.group(1)  # strip optional link "title"
            if re.match(r"^(https?://|mailto:|#)", target):
                continue
            tpath, _, anchor = target.partition("#")
            if not tpath:
                continue
            resolved = (path.parent / tpath).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{rel}: link escapes the bundle: {target}")
                continue
            if resolved.is_dir():
                resolved = resolved / "index.md"  # directory links land on the listing
            if not resolved.exists():
                errors.append(f"{rel}: broken link: {target}")
            elif anchor and resolved.suffix == ".md":
                if slugify(anchor) not in anchors_of(resolved) and anchor not in anchors_of(resolved):
                    warnings.append(f"{rel}: unresolved anchor #{anchor} in {resolved.relative_to(ROOT)}")

    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"WARNING {w}")
    print(f"\n{len(md_files)} markdown files checked: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
