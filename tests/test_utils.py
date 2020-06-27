# This enables pytest tests/ to be run from project root
# See https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import pytest
from fpl_draft_league import utils
from pathlib import Path

class TestGetJson:

    def setup_class(cls):

        print("SETTING UP")
        cls.email_address = 'lee.gower17@gmail.com',
        cls.league_id = 38996,
        cls.data_path = Path(__file__).parent.parent.absolute() / 'data'

    def test_raises_value_error(self):

        with pytest.raises(ValueError) as excinfo:
            utils.get_json(
                self.email_address,
                self.league_id,
                self.data_path,
                ['not_a_real_column', 'transactions']
            )

        assert (
            "Invalid dataset(s). The following datasets are not supported:"
               ) in str(excinfo.value)