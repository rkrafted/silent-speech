#!/usr/bin/env python3
"""Offline checks for scripts/forum_prefilter.py. Run: python3 scripts/test_forum_prefilter.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forum_prefilter as fp  # noqa: E402


def test_redaction():
    home = "/" + "Users/fixture/"
    raw = f"mail bob@example.com, ping @fixture.user, log at {home}proj.js now"
    out = fp.clean(raw)
    assert "@example" not in out and "@fixture" not in out and home not in out, out
    assert "[email]" in out and "@user" in out and "[path]" in out, out


def test_score_prefers_rare_parts():
    silent = fp.score("Silent speech with a DIY ADS1299 board", ["masseter EMG, dry electrodes"])
    generic = fp.score("EEG cap impedance", ["electrode " * 40 + "noise reference " * 40])
    assert silent > generic, (silent, generic)
    assert fp.is_rare("a cEEGrid adapter for ADS1299EEGFE-PDK") is True
    assert fp.is_rare("battery charging question") is False


def test_selection_keeps_rare_and_respects_cap():
    threads = [
        {"id": 1, "title": "noise reference electrode " * 30, "posts": ["x"]},
        {"id": 2, "title": "PiEEG ADS1299 board", "posts": ["masseter EMG"]},
        {"id": 3, "title": "unrelated chat", "posts": ["hello"]},
    ]
    kept = fp.select(threads, 2)
    assert len(kept) == 2
    assert 2 in {t["id"] for _, t in kept}, kept


if __name__ == "__main__":
    test_redaction()
    test_score_prefers_rare_parts()
    test_selection_keeps_rare_and_respects_cap()
    print("ok: 3 checks passed")
