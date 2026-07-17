from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class DistributionExportError(RuntimeError):
    """Raised when a finalized publication cannot be exported safely."""


class DistributionPackageExporter:
    """Create a deterministic, checksum-verified ZIP from a finalized release snapshot."""

    MANIFEST_FILE = "distribution-manifest.json"

    def export(self, output_dir: Path, destination: Path | None = None) -> dict[str, Any]:
        output_dir = Path(output_dir)
        finalization = self._read_json(output_dir / "finalization-manifest.json", "finalization manifest")
        execution_id = self._required(finalization.get("execution_id"), "execution_id")
        if finalization.get("status") != "finalized" or not finalization.get("release_ready"):
            raise DistributionExportError("only finalized release-ready artifacts can be exported")

        release_dir = output_dir / "release" / execution_id
        if not release_dir.is_dir():
            raise DistributionExportError(f"finalized release directory was not found: {release_dir}")

        expected = finalization.get("checksums")
        if not isinstance(expected, dict) or not expected:
            raise DistributionExportError("finalization checksums are missing")
        self._verify_checksums(release_dir, expected)

        distribution_dir = output_dir / "distribution"
        distribution_dir.mkdir(parents=True, exist_ok=True)
        zip_path = Path(destination) if destination else distribution_dir / f"sims-writer-publication-{execution_id}.zip"
        if not zip_path.is_absolute():
            zip_path = output_dir / zip_path
        zip_path.parent.mkdir(parents=True, exist_ok=True)

        included = sorted(expected)
        package_manifest = {
            "distribution_version": "1.0.0",
            "execution_id": execution_id,
            "request_id": finalization.get("request_id"),
            "status": "exported",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "source_release": str(Path("release") / execution_id),
            "archive_name": zip_path.name,
            "files": included,
            "checksums": {name: expected[name] for name in included},
        }
        manifest_bytes = (json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in included:
                self._write_deterministic(archive, f"publication/{name}", (release_dir / name).read_bytes())
            self._write_deterministic(archive, self.MANIFEST_FILE, manifest_bytes)

        self._verify_archive(zip_path, package_manifest)
        archive_checksum = hashlib.sha256(zip_path.read_bytes()).hexdigest()
        package_manifest.update({
            "archive_path": str(zip_path),
            "archive_sha256": archive_checksum,
            "archive_size_bytes": zip_path.stat().st_size,
        })
        (distribution_dir / self.MANIFEST_FILE).write_text(
            json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return package_manifest

    @staticmethod
    def _write_deterministic(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
        info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, data)

    @classmethod
    def _verify_archive(cls, zip_path: Path, manifest: dict[str, Any]) -> None:
        try:
            with zipfile.ZipFile(zip_path, "r") as archive:
                bad = archive.testzip()
                if bad:
                    raise DistributionExportError(f"distribution archive is corrupt: {bad}")
                names = set(archive.namelist())
                required = {f"publication/{name}" for name in manifest["files"]} | {cls.MANIFEST_FILE}
                if names != required:
                    raise DistributionExportError("distribution archive contents do not match manifest")
                for name, expected in manifest["checksums"].items():
                    actual = hashlib.sha256(archive.read(f"publication/{name}")).hexdigest()
                    if actual != expected:
                        raise DistributionExportError(f"archive checksum mismatch: {name}")
        except zipfile.BadZipFile as exc:
            raise DistributionExportError("distribution archive is not a valid ZIP") from exc

    @staticmethod
    def _verify_checksums(release_dir: Path, expected: dict[str, Any]) -> None:
        for name, checksum in expected.items():
            path = release_dir / name
            if not path.is_file():
                raise DistributionExportError(f"finalized artifact is missing: {name}")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != checksum:
                raise DistributionExportError(f"finalized artifact checksum mismatch: {name}")

    @staticmethod
    def _required(value: Any, label: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise DistributionExportError(f"{label} is required")
        return text

    @staticmethod
    def _read_json(path: Path, label: str) -> dict[str, Any]:
        if not path.is_file():
            raise DistributionExportError(f"{label} was not found: {path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DistributionExportError(f"{label} is invalid: {path}") from exc
        if not isinstance(payload, dict):
            raise DistributionExportError(f"{label} must be a JSON object")
        return payload
