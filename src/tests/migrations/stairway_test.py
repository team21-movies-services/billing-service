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


@pytest.mark.parametrize('revision', get_revisions())
def test_revision_branching(revision: Script, alembic_script_directory):
    """Тест проверяет каждую миграцию на наличие не более одной дочерней миграции для избежания ветвления"""
    rev_children = revision._all_nextrev
    if len(rev_children) > 1:
        revisions_paths = [alembic_script_directory.get_revision(rev).path for rev in rev_children]
        pytest.fail(f"Revision {revision.path} has more than one child revision. {revisions_paths}")
