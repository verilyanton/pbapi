import os
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from db_backup import (
    get_db_config,
    create_backup,
    list_backups,
    cleanup_old_backups,
)


class TestDbBackup(TestCase):
    @patch("db_backup.load_doppler_secrets")
    def test_get_db_config(self, mock_load_secrets):
        with patch.dict(
            os.environ,
            {
                "POSTGRES_HOST": "testhost",
                "POSTGRES_PORT": "5433",
                "POSTGRES_DB": "testdb",
                "POSTGRES_USER": "testuser",
                "POSTGRES_PASSWORD": "testpass",
            },
        ):
            config = get_db_config()
            self.assertEqual(config["host"], "testhost")
            self.assertEqual(config["port"], "5433")
            self.assertEqual(config["database"], "testdb")
            self.assertEqual(config["user"], "testuser")
            self.assertEqual(config["password"], "testpass")
        mock_load_secrets.assert_called_once()

    @patch("db_backup.load_doppler_secrets")
    def test_get_db_config_defaults(self, mock_load_secrets):
        with patch.dict(os.environ, {"POSTGRES_DB": "testdb"}, clear=False):
            config = get_db_config()
            self.assertEqual(config["host"], "localhost")
            self.assertEqual(config["port"], "5432")
            self.assertEqual(config["database"], "testdb")
            self.assertEqual(config["user"], "postgres")
            self.assertEqual(config["password"], "postgres")

    @patch("db_backup.load_doppler_secrets")
    @patch("db_backup.subprocess.run")
    def test_create_backup(self, mock_run, mock_load_secrets):
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "POSTGRES_HOST": "localhost",
                    "POSTGRES_PORT": "5432",
                    "POSTGRES_DB": "testdb",
                    "POSTGRES_USER": "testuser",
                    "POSTGRES_PASSWORD": "testpass",
                },
            ):
                backup_file = create_backup(backup_dir=tmpdir)
                self.assertTrue(backup_file.startswith(tmpdir))
                self.assertTrue(backup_file.endswith(".sql"))
                mock_run.assert_called_once()

    def test_list_backups(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some test backup files
            Path(tmpdir, "testdb_20260101_120000.sql").touch()
            Path(tmpdir, "testdb_20260102_120000.sql").touch()
            Path(tmpdir, "testdb_20260103_120000.sql").touch()

            all_backups = list_backups(tmpdir)
            self.assertEqual(len(all_backups), 3)

    def test_list_backups_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            backups = list_backups(tmpdir)
            self.assertEqual(len(backups), 0)

    def test_list_backups_nonexistent_dir(self):
        backups = list_backups("/nonexistent/path")
        self.assertEqual(len(backups), 0)

    def test_cleanup_old_backups(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test backup files
            files = [
                "testdb_20260101_120000.sql",
                "testdb_20260102_120000.sql",
                "testdb_20260103_120000.sql",
                "testdb_20260104_120000.sql",
                "testdb_20260105_120000.sql",
            ]
            for f in files:
                Path(tmpdir, f).touch()

            # Keep only 2 backups
            cleanup_old_backups(tmpdir, keep=2)

            remaining = list_backups(tmpdir)
            self.assertEqual(len(remaining), 2)
            # Should keep the most recent ones (reverse sorted)
            self.assertTrue(remaining[0].endswith("20260105_120000.sql"))
            self.assertTrue(remaining[1].endswith("20260104_120000.sql"))
