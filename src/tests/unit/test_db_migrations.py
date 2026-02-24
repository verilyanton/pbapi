from unittest import TestCase
from unittest.mock import MagicMock, patch

from db_migration import (
    migrate_postgres_up,
    migrate_postgres_down,
    run_alembic_command,
)


class TestMigrations(TestCase):
    @patch("db_migration.run_alembic_command")
    @patch("db_migration.cleanup_old_backups")
    @patch("db_migration.create_backup")
    def test_migrate_postgres_up_with_backup(
        self, mock_create_backup, mock_cleanup, mock_alembic
    ):
        mock_alembic.return_value = 0

        migrate_postgres_up("dev", "head", backup=True)

        mock_create_backup.assert_called_once_with()
        mock_cleanup.assert_called_once_with(keep=10)
        mock_alembic.assert_called_once_with(["upgrade", "head"], "dev")

    @patch("db_migration.run_alembic_command")
    @patch("db_migration.create_backup")
    def test_migrate_postgres_up_without_backup(self, mock_create_backup, mock_alembic):
        mock_alembic.return_value = 0

        migrate_postgres_up("dev", "head", backup=False)

        mock_create_backup.assert_not_called()
        mock_alembic.assert_called_once_with(["upgrade", "head"], "dev")

    @patch("db_migration.run_alembic_command")
    @patch("db_migration.cleanup_old_backups")
    @patch("db_migration.create_backup")
    def test_migrate_postgres_down_with_backup(
        self, mock_create_backup, mock_cleanup, mock_alembic
    ):
        mock_alembic.return_value = 0

        migrate_postgres_down("dev", "-1", backup=True)

        mock_create_backup.assert_called_once_with()
        mock_cleanup.assert_called_once_with(keep=10)
        mock_alembic.assert_called_once_with(["downgrade", "-1"], "dev")

    @patch("subprocess.run")
    def test_run_alembic_command(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        result = run_alembic_command(["upgrade", "head"], "dev")

        self.assertEqual(result, 0)
        mock_run.assert_called_once()
