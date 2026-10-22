import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from orchestra.archive import create_archive, verify_archive


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "data").mkdir()
        (self.root / "data" / "rows.jsonl").write_text("{}\n")
        self.archive = self.root / "backup.zip"

    def test_roundtrip_local_backup_and_no_overwrite(self):
        result = create_archive(self.root, ["data/rows.jsonl"], self.archive)
        self.assertTrue(result["local_only"])
        self.assertEqual(len(result["sha256"]), 64)
        destination = self.root / "restored"
        restored = verify_archive(self.archive, destination)
        self.assertTrue(restored["verified"])
        self.assertEqual((destination / "data/rows.jsonl").read_text(), "{}\n")
        with self.assertRaises(FileExistsError):
            verify_archive(self.archive, destination)
        with self.assertRaises(FileExistsError):
            create_archive(self.root, ["data/rows.jsonl"], self.archive)

    def test_reject_unsafe_allowlist_without_partial_output(self):
        for name in ("../outside", "/tmp/file", ".env", "course.pdf", "id_rsa", "data"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                create_archive(self.root, [name], self.archive)
            self.assertFalse(self.archive.exists())
        (self.root / "link").symlink_to(self.root / "data/rows.jsonl")
        with self.assertRaises(ValueError):
            create_archive(self.root, ["link"], self.archive)
        with self.assertRaises(ValueError):
            create_archive(self.root, ["data/rows.jsonl"] * 2, self.archive)

    def test_reject_traversal_and_symlinks_before_restore(self):
        cases = [
            ("../escape", b"x", None),
            ("link", b"x", 0o120777),
        ]
        for n, (name, payload, mode) in enumerate(cases):
            with self.subTest(name=name):
                archive = self.root / f"bad{n}.zip"
                with zipfile.ZipFile(archive, "w") as z:
                    z.writestr(
                        "MANIFEST.json",
                        json.dumps(
                            {
                                "version": 1,
                                "local_only": True,
                                "members": {"data/rows.jsonl": "incorrect"},
                            }
                        ),
                    )
                    info = zipfile.ZipInfo(name)
                    if mode:
                        info.external_attr = mode << 16
                    z.writestr(info, payload)
                destination = self.root / f"bad{n}"
                with self.assertRaises(ValueError):
                    verify_archive(archive, destination)
                self.assertFalse(destination.exists())

    def test_duplicate_zip_member_is_rejected(self):
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.archive, "w") as archive:
                archive.writestr("MANIFEST.json", "{}")
                archive.writestr("same", "a")
                archive.writestr("same", "b")
        destination = self.root / "duplicate"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_archive(self.archive, destination)
        self.assertFalse(destination.exists())

    def test_disguised_key_and_pdf_contents_are_rejected(self):
        for content in (b"-----BEGIN OPENSSH PRIVATE KEY-----", b"%PDF-1.7"):
            (self.root / "innocent.txt").write_bytes(content)
            with self.assertRaises(ValueError):
                create_archive(self.root, ["innocent.txt"], self.archive)
            self.assertFalse(self.archive.exists())

    def test_symlink_parent_is_rejected(self):
        (self.root / "linked").symlink_to(self.root / "data", target_is_directory=True)
        with self.assertRaises(ValueError):
            create_archive(self.root, ["linked/rows.jsonl"], self.archive)

    def test_restore_preserves_executable_without_special_permissions(self):
        import subprocess

        script = self.root / "run.sh"
        script.write_text("#!/bin/sh\nprintf restored\n")
        script.chmod(0o4755)
        create_archive(self.root, ["run.sh"], self.archive)
        destination = self.root / "executable"
        verify_archive(self.archive, destination)
        self.assertEqual((destination / "run.sh").stat().st_mode & 0o7777, 0o755)
        self.assertEqual(
            subprocess.check_output([str(destination / "run.sh")]), b"restored"
        )

    def test_manifest_special_permission_is_rejected(self):
        import hashlib

        with zipfile.ZipFile(self.archive, "w") as archive:
            archive.writestr("safe", "content")
            archive.writestr(
                "MANIFEST.json",
                json.dumps(
                    {
                        "version": 1,
                        "local_only": True,
                        "members": {"safe": hashlib.sha256(b"content").hexdigest()},
                        "modes": {"safe": 0o4755},
                    }
                ),
            )
        destination = self.root / "special"
        with self.assertRaisesRegex(ValueError, "permissions"):
            verify_archive(self.archive, destination)
        self.assertFalse(destination.exists())

    def test_archive_own_source_and_header_mentions(self):
        import orchestra.archive

        module = Path(orchestra.archive.__file__)
        (self.root / "archive.py").write_bytes(module.read_bytes())
        (self.root / "mentions.py").write_text(
            'header = b"-----BEGIN RSA PRIVATE KEY-----"\n'
        )
        create_archive(self.root, ["archive.py", "mentions.py"], self.archive)
        self.assertTrue(
            verify_archive(self.archive, self.root / "source-restore")["verified"]
        )

    def test_actual_pem_header_after_preamble_is_rejected(self):
        (self.root / "disguised.txt").write_bytes(
            b"Preamble\n-----BEGIN RSA PRIVATE KEY-----\nfixture\n-----END RSA PRIVATE KEY-----\n"
        )
        with self.assertRaises(ValueError):
            create_archive(self.root, ["disguised.txt"], self.archive)
        self.assertFalse(self.archive.exists())

    def test_reject_changed_member_with_valid_manifest_before_restore(self):
        create_archive(self.root, ["data/rows.jsonl"], self.archive)
        tampered = self.root / "tampered.zip"
        with (
            zipfile.ZipFile(self.archive) as original,
            zipfile.ZipFile(tampered, "w") as changed,
        ):
            for info in original.infolist():
                content = (
                    b"changed"
                    if info.filename == "data/rows.jsonl"
                    else original.read(info)
                )
                changed.writestr(info, content)
        destination = self.root / "corrupt-restore"
        with self.assertRaisesRegex(ValueError, "checksum mismatch: data/rows.jsonl"):
            verify_archive(tampered, destination)
        self.assertFalse(destination.exists())
