"""Pre-work jobs - handle config and/or CLI"""
# 1. std
from typing import Optional
import os
import sys
import json
import os.path
# 2. 3rd
import appdirs
# 3. local
from . import exc


class UlibCfgLoadError(exc.UlibTextError):
    """Config loading exceptions."""
    name = "CfgLoad"


def cli():
    """Handle CLI"""
    ...


def load_cfg(fname: str) -> Optional[dict]:
    """Load config (sibling > ~ > /etc)
    :return: Config loaded
    :todo: ini, yaml, json5, toml, xml
    :todo: convert into object
    """
    for d in (
            os.path.abspath(os.path.dirname(sys.argv[0])),  # ./
            appdirs.user_config_dir(),   # ~/.config
            appdirs.site_config_dir()):  # /etc/xdg (!)
        fpath = os.path.join(d, fname)
        if not os.path.exists(fpath):  # or handle FileNotFoundError
            continue
        try:
            return json.load(open(fpath))
        except (IsADirectoryError, PermissionError, json.decoder.JSONDecodeError) as e:
            raise UlibCfgLoadError(f"'{fpath}': {str(e)}")
    sys.exit("Config not found")
