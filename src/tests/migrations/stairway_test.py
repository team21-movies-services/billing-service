import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory


def get_revisions():
    config = Config("alembic.ini")
    revisions_dir = ScriptDirectory.from_config(config)

    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(monkeypatch, revision: Script, single_use_database):
    monkeypatch.setenv('MIGRATION_TEST', 'True')
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", str(single_use_database.url))

    upgrade(alembic_config, revision.revision)
    # We need -1 for downgrading first migration (its down_revision is None)
    downgrade(alembic_config, revision.down_revision or '-1')
    upgrade(alembic_config, revision.revision)
    monkeypatch.delenv('MIGRATION_TEST')
