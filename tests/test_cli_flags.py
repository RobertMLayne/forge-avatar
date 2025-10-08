"""Arg-parse coverage for new flags."""
from __future__ import annotations

import unittest

from forgeavatar.cli import build_parser


class TestCLIFlags(unittest.TestCase):
    def test_parse_quality_flags(self) -> None:
        p = build_parser()
        ns = p.parse_args(
            [
                "--input",
                "in.png",
                "--output",
                "out.png",
                "--sr-scale",
                "4",
                "--no-face-restore",
                "--no-shadow",
                "--quality",
                "80",
            ]
        )
        self.assertEqual(ns.sr_scale, 4)
        self.assertTrue(ns.no_face_restore)
        self.assertEqual(ns.quality, 80)
