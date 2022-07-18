"""Pre-work jobs - handle config and/or CLI"""
# 1. std
import os
import sys
import json
import os.path
# 2. 3rd
import appdirs
# 3. local
from typing import Optional

from . import exc


class YAPBCfgLoadError(exc.YAPBTextError):
    """Config loading exceptions."""
    name = "CfgLoad"


def cli():
    """Handle CLI"""
    ...


def load_cfg(fname: str) -> Optional[dict]:
    """Load config (sibling > ~ > /etc)
    :return: Config loaded
    """
    # FIXME: abspath(.), appdirs.user_config_dir, appdirs.site_config_dir
    for d in (
            os.path.abspath(os.path.dirname(sys.argv[0])),
            appdirs.user_config_dir(),   # ~/.config
            appdirs.site_config_dir()):  # /etc
        fpath = os.path.join(d, fname)
        if not os.path.exists(fpath):  # or handle FileNotFoundError
            continue
        try:
            return json.load(open(fpath))
        except (IsADirectoryError, PermissionError, json.decoder.JSONDecodeError) as e:
            raise YAPBCfgLoadError(f"'{fpath}': {str(e)}")
    return
