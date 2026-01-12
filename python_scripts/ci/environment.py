"""Script to setup and teardown the CI environment."""

import argparse
import os

import toml


def setup(
    settings_file: str = "ci-settings.toml",
    key_filename: str = "ci-key.key",
) -> None:
    """Create the CI environment."""
    with open("settings.example.toml", "r") as f:
        settings = toml.load(f)

    for section in settings.keys():
        for key in settings[section].keys():
            env_var = f"{section.upper()}_{key.upper()}"
            env_value = os.environ.get(env_var)
            if env_value is not None:
                print(f"Loading {env_var} from environment.")
                settings[section][key] = env_value

    print("Setting key filename in deployer settings.")
    settings["Deployer"]["key_filename"] = key_filename
    env_key_var = "DEPLOYER_KEY_CONTENT"
    print(f"Writing deployer from environment variable {env_key_var}.")
    with open(key_filename, "w") as f:
        key_content = os.environ.get(env_key_var, "")
        f.write(key_content)

    with open(settings_file, "w") as f:
        toml.dump(settings, f)


def teardown(
    settings_file: str = "ci-settings.toml",
    key_filename: str = "ci-key.key",
) -> None:
    """Delete the CI environment."""
    try:
        os.remove(settings_file)
    except FileNotFoundError:
        print(f"Settings file {settings_file} not found, skipping.")

    try:
        os.remove(key_filename)
    except FileNotFoundError:
        print(f"Key file {key_filename} not found, skipping.")


def main() -> None:
    """Script entry point."""
    parser = argparse.ArgumentParser(description="Setup/Teardown CI environment.")
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup the CI environment.",
    )
    parser.add_argument(
        "--teardown",
        action="store_true",
        help="Teardown the CI environment.",
    )
    parser.add_argument(
        "--settings",
        type=str,
        help="Settings file path",
        default="ci-settings.toml",
    )
    parser.add_argument(
        "--key-filename",
        type=str,
        help="Deployer key filename",
        default="ci-key.key",
    )

    arguments = parser.parse_args()

    if arguments.teardown:
        teardown(
            settings_file=arguments.settings,
            key_filename=arguments.key_filename,
        )
    else:
        setup(
            settings_file=arguments.settings,
            key_filename=arguments.key_filename,
        )


if __name__ == "__main__":
    main()
