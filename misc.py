import json
import config as cfg

from functools import lru_cache


@lru_cache(maxsize=1)
def get_variables_from_token_file():
    with open(cfg.TOKEN_FILE_PATH) as f:
        return json.loads(f.read()).get('installed')


def get_client_id():
    return get_variables_from_token_file().get('client_id')


def get_client_secret():
    return get_variables_from_token_file().get('client_secret')


if __name__ == '__main__':
    print(get_variables_from_token_file())
