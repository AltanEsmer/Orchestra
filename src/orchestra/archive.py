"""Explicit local-only ZIP backups with verified, traversal-safe restoration."""

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

MANIFEST = "MANIFEST.json"


def _name(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("archive paths must be nonempty relative POSIX file paths")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) != value or ":" in value:
        raise ValueError(f"unsafe archive path: {value}")
    if value == MANIFEST:
        raise ValueError("MANIFEST.json is reserved")
    for part in path.parts:
        lower = part.lower()
        if (
            lower.startswith(".env")
            or lower in {".git", ".ssh", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
            or lower.endswith((".pem", ".key", ".p12", ".pfx", ".pdf"))
        ):
            raise ValueError(f"secret or course-PDF path is not allowed: {value}")
    return path


def _digest(content):
    return hashlib.sha256(content).hexdigest()


def _content_safe(name, content):
    private_header = re.search(
        rb"^-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----\r?$", content, re.MULTILINE
    )
    if private_header or content.startswith(b"%PDF-"):
        raise ValueError(f"private key or PDF content is not allowed: {name}")


def create_archive(root, paths, out):
    """Back up only named regular files. This never grants redistribution rights."""
    root, out = Path(root).resolve(), Path(out)
    if out.exists() or out.is_symlink():
        raise FileExistsError(out)
    members, modes = {}, {}
    for value in paths:
        name = str(_name(value))
        if name in members:
            raise ValueError(f"duplicate archive member: {name}")
        source = root / name
        if any(p.is_symlink() for p in [source, *source.parents] if p != root.parent):
            raise ValueError(f"symlink is not allowed: {name}")
        if not source.is_file():
            raise ValueError(f"allowlist must name an existing regular file: {name}")
        if source.resolve() == out.resolve():
            raise ValueError("archive output collides with an input")
        content = source.read_bytes()
        _content_safe(name, content)
        members[name] = content
        modes[name] = stat.S_IMODE(source.stat().st_mode) & 0o777
    if not members:
        raise ValueError("archive allowlist must not be empty")
    manifest = {
        "version": 1,
        "local_only": True,
        "permission": "Local backup only. Dataset permission and redistribution must be verified separately.",
        "modes": modes,
        "members": {
            name: _digest(content) for name, content in sorted(members.items())
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".orchestra-archive-", dir=out.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            for name, content in sorted(members.items()):
                archive.writestr(name, content)
            archive.writestr(MANIFEST, json.dumps(manifest, indent=2) + "\n")
        os.link(temporary, out)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return {
        "archive": str(out),
        "sha256": _digest(out.read_bytes()),
        "local_only": True,
        "manifest": manifest,
    }


def verify_archive(archive, destination):
    """Validate every member before restoring to a new directory."""
    archive, destination = Path(archive), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    try:
        with zipfile.ZipFile(archive) as source:
            infos = source.infolist()
            names = [info.filename for info in infos]
            if len(set(names)) != len(names) or names.count(MANIFEST) != 1:
                raise ValueError("duplicate members or missing manifest")
            for info in infos:
                if info.filename != MANIFEST:
                    _name(info.filename)
                mode = info.external_attr >> 16
                if (
                    info.is_dir()
                    or stat.S_ISLNK(mode)
                    or (stat.S_IFMT(mode) not in (0, stat.S_IFREG))
                ):
                    raise ValueError(f"nonregular archive member: {info.filename}")
            manifest = json.loads(source.read(MANIFEST))
            if (
                not isinstance(manifest, dict)
                or manifest.get("version") != 1
                or manifest.get("local_only") is not True
                or not isinstance(manifest.get("members"), dict)
            ):
                raise ValueError("invalid local backup manifest")
            expected = manifest["members"]
            if not expected or set(expected) != set(names) - {MANIFEST}:
                raise ValueError("manifest member list differs from ZIP")
            modes = manifest.get("modes")
            if not isinstance(modes, dict) or set(modes) != set(expected):
                raise ValueError("manifest permission list differs from members")
            if any(
                type(mode) is not int or mode < 0 or mode > 0o777
                for mode in modes.values()
            ):
                raise ValueError("unsafe file permissions in manifest")
            contents = {}
            for name, digest in expected.items():
                _name(name)
                content = source.read(name)
                _content_safe(name, content)
                if _digest(content) != digest:
                    raise ValueError(f"checksum mismatch: {name}")
                contents[name] = content
    except (
        zipfile.BadZipFile,
        json.JSONDecodeError,
        UnicodeError,
        KeyError,
        RuntimeError,
    ) as error:
        raise ValueError(f"invalid archive: {error}") from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".orchestra-restore-", dir=destination.parent)
    )
    created_destination = False
    try:
        for name, content in contents.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            target.chmod(modes[name])
        (staging / MANIFEST).write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        destination.mkdir()
        created_destination = True
        for child in staging.iterdir():
            shutil.move(str(child), destination / child.name)
    except OSError:
        if created_destination:
            shutil.rmtree(destination)
        raise
    finally:
        shutil.rmtree(staging)
    return {
        "verified": True,
        "destination": str(destination),
        "sha256": _digest(archive.read_bytes()),
        "local_only": True,
        "manifest": manifest,
    }
