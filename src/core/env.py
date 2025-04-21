from pathlib import Path
import environ


def load_env(dotenv_path: Path) -> environ.Env:
    env = environ.Env(
        DEBUG=(bool, False),
    )
    if dotenv_path.exists():
        env.read_env(dotenv_path)
    return env
