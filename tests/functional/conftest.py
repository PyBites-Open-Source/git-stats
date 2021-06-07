from shutil import rmtree

import pytest

from stats.utils import run_command


@pytest.fixture(scope="module")
def karmabot_dir(tmp_path_factory):
    karmabot_dir = tmp_path_factory.mktemp("karmabot") / "karmabot"
    cmd = ("git clone git@github.com:pybob/karmabot.git"
           f" {karmabot_dir} 2>&1 > /dev/null")
    run_command(cmd)
    yield karmabot_dir
    rmtree(karmabot_dir)
