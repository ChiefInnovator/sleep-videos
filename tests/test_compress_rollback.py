"""Fault-injection checks for delivery/report publication and recovery."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import compress_videos as compressor


class DeliveryRollback(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.target = self.root/'site/media/test-preview.mp4'
        self.report = self.root/'reports/test-preview.json'
        self.target.parent.mkdir(parents=True)
        self.report.parent.mkdir()
        self.target.write_bytes(b'original delivery')
        self.report.write_text(json.dumps({'original':True}))
        self.previous = self.target.with_suffix('.previous.tmp.mp4')
        self.temporary = self.target.with_suffix('.tmp.mp4')
        self.staged_report = self.report.with_suffix('.tmp.json')

    def run_export(self, failing=()):
        original_replace = Path.replace

        def replace(path, target):
            if path in failing:
                raise OSError('injected rename failure')
            return original_replace(path, target)

        def encode(master, target, *args, **kwargs):
            target.write_bytes(b'new delivery')

        with patch.object(compressor, 'ROOT', self.root), \
             patch.object(compressor, 'KINDS', ['test']), \
             patch.object(compressor, 'run', return_value=SimpleNamespace(stdout=' aac_at ')), \
             patch.object(compressor, 'video', side_effect=encode), \
             patch.object(compressor, 'video_qc', return_value={'probe':{'format':{}}}), \
             patch.object(sys, 'argv', ['compress_videos.py', '--only', 'test']), \
             patch.object(Path, 'replace', replace):
            compressor.main()

    def test_success_publishes_pair_and_removes_backup(self):
        self.run_export()
        self.assertEqual(self.target.read_bytes(), b'new delivery')
        self.assertEqual(json.loads(self.report.read_text())['delivery']['bytes'], 12)
        self.assertFalse(self.previous.exists())

    def test_delivery_rename_failure_restores_original_pair(self):
        with self.assertRaises(OSError):
            self.run_export([self.temporary])
        self.assertEqual(self.target.read_bytes(), b'original delivery')
        self.assertEqual(json.loads(self.report.read_text()), {'original':True})

    def test_report_rename_failure_restores_original_pair(self):
        with self.assertRaises(OSError):
            self.run_export([self.staged_report])
        self.assertEqual(self.target.read_bytes(), b'original delivery')
        self.assertEqual(json.loads(self.report.read_text()), {'original':True})

    def test_failed_restore_keeps_last_good_backup(self):
        with self.assertRaises(OSError):
            self.run_export([self.staged_report, self.previous])
        self.assertEqual(self.previous.read_bytes(), b'original delivery')
        self.assertEqual(json.loads(self.report.read_text()), {'original':True})

    def test_report_failure_without_old_delivery_removes_new_target(self):
        self.target.unlink()
        with self.assertRaises(OSError):
            self.run_export([self.staged_report])
        self.assertFalse(self.target.exists())
        self.assertEqual(json.loads(self.report.read_text()), {'original':True})

    def test_existing_recovery_backup_is_never_overwritten(self):
        self.previous.write_bytes(b'preserved recovery delivery')
        with self.assertRaisesRegex(RuntimeError, 'Recover the previous delivery'):
            self.run_export()
        self.assertEqual(self.previous.read_bytes(), b'preserved recovery delivery')
        self.assertEqual(self.target.read_bytes(), b'original delivery')


if __name__ == '__main__':
    unittest.main()
