"""Tests for the pruning of the remote folders (it deletes files, so be sure)."""

import stat
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from modules.deployer import Deployer
from modules.settings import DeployerSettings


class FakeSftp:
    """In-memory stand-in for the SFTP client: remote path -> is a folder."""

    def __init__(self, tree: dict[str, bool]) -> None:
        self.tree = dict(tree)

    def listdir_attr(self, folder: str) -> list[Any]:
        if folder not in self.tree:
            raise FileNotFoundError(folder)
        prefix = folder.rstrip("/") + "/"
        return [
            SimpleNamespace(
                filename=path.removeprefix(prefix),
                st_mode=stat.S_IFDIR if is_dir else stat.S_IFREG,
            )
            for path, is_dir in self.tree.items()
            if path.startswith(prefix) and "/" not in path.removeprefix(prefix)
        ]

    def remove(self, path: str) -> None:
        del self.tree[path]

    def rmdir(self, path: str) -> None:
        assert not any(p.startswith(path + "/") for p in self.tree), "not empty"
        del self.tree[path]


def make_deployer(sftp: FakeSftp, **settings: Any) -> Deployer:
    deployer = Deployer(DeployerSettings(hostname="h", remote_path="/www", **settings))
    deployer._sftp = sftp  # ty: ignore[invalid-assignment]
    return deployer


def test_prune_deletes_only_what_is_missing_locally(tmp_path: Path) -> None:
    (tmp_path / "blog" / "kept").mkdir(parents=True)
    (tmp_path / "blog" / "kept" / "index.html").write_text("x")
    sftp = FakeSftp(
        {
            "/www": True,
            "/www/other.html": False,
            "/www/blog": True,
            "/www/blog/kept": True,
            "/www/blog/kept/index.html": False,
            "/www/blog/kept/old.png": False,
            "/www/blog/gone": True,
            "/www/blog/gone/index.html": False,
            "/www/blog/stale.html": False,
        }
    )

    make_deployer(sftp).prune(tmp_path, "blog")

    assert set(sftp.tree) == {
        "/www",
        "/www/other.html",  # outside the pruned folder
        "/www/blog",
        "/www/blog/kept",
        "/www/blog/kept/index.html",
    }


def test_prune_missing_remote_folder_is_fine(tmp_path: Path) -> None:
    (tmp_path / "blog").mkdir()
    make_deployer(FakeSftp({"/www": True})).prune(tmp_path, "blog")


@pytest.mark.parametrize("folder", ["", ".", "/etc", "../x", "blog/../.."])
def test_prune_rejects_unsafe_paths(tmp_path: Path, folder: str) -> None:
    sftp = FakeSftp({"/www": True, "/www/a": False})
    with pytest.raises(ValueError, match="Invalid prune path"):
        make_deployer(sftp).prune(tmp_path, folder)
    assert "/www/a" in sftp.tree


def test_prune_refuses_when_local_folder_is_missing(tmp_path: Path) -> None:
    sftp = FakeSftp({"/www": True, "/www/blog": True, "/www/blog/a.html": False})
    with pytest.raises(ValueError, match="Refusing to prune"):
        make_deployer(sftp).prune(tmp_path, "blog")
    assert "/www/blog/a.html" in sftp.tree
