# QuantJourney Backtester
# Copyright (c) 2026 QuantJourney.
# Licensed under the Apache License 2.0.

"""Keep the reviewed type gate stable across Git checkout line endings."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


def _checker(tmp_path, monkeypatch):
    path = Path(__file__).resolve().parents[1] / "tools/check_mypy_baseline.py"
    spec = importlib.util.spec_from_file_location("mypy_baseline_checker", path)
    assert spec is not None and spec.loader is not None
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    monkeypatch.setattr(checker, "ROOT", tmp_path)
    (tmp_path / "pyproject.toml").write_text(
        '[tool.mypy]\npython_version = "3.11"\n', encoding="utf-8"
    )
    return checker


def test_lock_identity_survives_windows_checkout_line_endings(tmp_path, monkeypatch):
    checker = _checker(tmp_path, monkeypatch)
    lock = tmp_path / "uv.lock"
    original = b"version = 1\nrevision = 3\n"
    lock.write_bytes(original)
    lf_context = checker._context()
    lock.write_bytes(original.replace(b"\n", b"\r\n"))
    assert checker._context() == lf_context
    assert lf_context["lock_sha256"] == hashlib.sha256(original).hexdigest()


def test_lock_content_changes_still_invalidate_type_context(tmp_path, monkeypatch):
    checker = _checker(tmp_path, monkeypatch)
    lock = tmp_path / "uv.lock"
    lock.write_bytes(b"version = 1\nrevision = 3\n")
    original = checker._context()
    lock.write_bytes(b"version = 1\nrevision = 4\n")
    assert checker._context()["lock_sha256"] != original["lock_sha256"]
