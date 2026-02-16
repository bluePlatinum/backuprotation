from backuprotation.main import parse_args, discover, rotate
import pytest
import tempfile
import random
import string
import os
import time


@pytest.fixture
def create_testing_dir():
    tmpdir = tempfile.TemporaryDirectory()

    dirs = list()
    files = list()

    dirnum = random.randint(1, 10)
    filenum = random.randint(1, 10)

    for _ in range(dirnum):
        name = "".join(random.choices(string.ascii_lowercase, k=8))

        while os.path.exists(name):
            name = "".join(random.choices(string.ascii_lowercase, k=8))

        dirpath = os.path.join(tmpdir.name, name)
        os.makedirs(dirpath)
        dirs.append(name)

        # fill directory with dirs and files
        for _ in range(random.randint(0, 10)):
            name = "".join(random.choices(string.ascii_lowercase, k=8))
            while os.path.exists(name):
                name = "".join(random.choices(string.ascii_lowercase, k=8))
            if random.randint(0, 1):
                os.makedirs(os.path.join(dirpath, name))
            else:
                open(os.path.join(dirpath, name), "w").close()

    for _ in range(filenum):
        name = "".join(random.choices(string.ascii_lowercase, k=8))

        while os.path.exists(name):
            name = "".join(random.choices(string.ascii_lowercase, k=8))

        open(os.path.join(tmpdir.name, name), "w").close()
        files.append(name)

    return tmpdir, dirs, files


@pytest.fixture
def create_timed_dir():
    tmpdir = tempfile.TemporaryDirectory()

    dirs = list()

    dirnum = 30

    for _ in range(dirnum):
        name = "".join(random.choices(string.ascii_lowercase, k=8))

        while os.path.exists(name):
            name = "".join(random.choices(string.ascii_lowercase, k=8))

        time.sleep(0.1)
        dirpath = os.path.join(tmpdir.name, name)
        os.makedirs(dirpath)
        dirs.append(name)

        # fill directory with dirs and files
        for _ in range(random.randint(1, 10)):
            name = "".join(random.choices(string.ascii_lowercase, k=8))
            while os.path.exists(os.path.join(dirpath, name)):
                name = "".join(random.choices(string.ascii_lowercase, k=8))
            if random.randint(0, 1):
                os.makedirs(os.path.join(dirpath, name))
            else:
                open(os.path.join(dirpath, name), "w").close()

    return tmpdir, dirs


@pytest.fixture
def create_timed_files():
    tmpdir = tempfile.TemporaryDirectory()

    files = list()

    filenum = 30

    for _ in range(filenum):
        name = "".join(random.choices(string.ascii_lowercase, k=8))

        while os.path.exists(name):
            name = "".join(random.choices(string.ascii_lowercase, k=8))

        time.sleep(0.1)
        open(os.path.join(tmpdir.name, name), "w").close()
        files.append(name)

    return tmpdir, files


class TestArgumentParsing:
    def test_required_path(self):
        with pytest.raises(SystemExit):
            args = parse_args([])

    def test_n_type(self):
        with pytest.raises(SystemExit):
            args = parse_args(["./path", "-n", "a"])


class TestDiscovery:
    def test_dir_discovery(self, create_testing_dir):
        tmpdir, dirs, files = create_testing_dir

        discovered = discover(tmpdir.name, True, False)

        assert set(dirs) == set(list(map(os.path.basename, discovered)))

    def test_file_discovery(self, create_testing_dir):
        tmpdir, dirs, files = create_testing_dir

        discovered = discover(tmpdir.name, False, True)

        assert set(files) == set(list(map(os.path.basename, discovered)))

    def test_dir_file_discovery(self, create_testing_dir):
        tmpdir, dirs, files = create_testing_dir

        discovered = discover(tmpdir.name, True, True)

        combined = dirs + files

        assert set(combined) == set(list(map(os.path.basename, discovered)))

    def test_ordering_discovery(self):
        tmpdir = tempfile.TemporaryDirectory()

        dirs = list()

        dirnum = random.randint(1, 10)

        for _ in range(dirnum):
            name = "".join(random.choices(string.ascii_lowercase, k=8))

            while os.path.exists(name):
                name = "".join(random.choices(string.ascii_lowercase, k=8))

            time.sleep(0.1)                             # testing for sorting
            os.makedirs(os.path.join(tmpdir.name, name))
            dirs.append(name)

        discovered = discover(tmpdir.name, True, False)

        assert dirs == list(map(os.path.basename, discovered))


class TestRotation:
    def test_dry_run(self, create_timed_dir):
        tmpdir, dirs = create_timed_dir

        discovered = discover(tmpdir.name, True, False)

        rotate(discovered, 10, True)

        after = os.listdir(tmpdir.name)

        assert set(dirs) == set(after)

    def test_dir_deletion(self, create_timed_dir):
        tmpdir, dirs = create_timed_dir

        n = 10

        discovered = discover(tmpdir.name, True, False)

        rotate(discovered, n, False)

        after = os.listdir(tmpdir.name)

        assert set(dirs[-n:]) == set(after)

    def test_file_deletion(self, create_timed_files):
        tmpdir, files = create_timed_files

        n = 10

        discovered = discover(tmpdir.name, False, True)

        rotate(discovered, n, False)

        after = os.listdir(tmpdir.name)

        assert set(files[-n:]) == set(after)
