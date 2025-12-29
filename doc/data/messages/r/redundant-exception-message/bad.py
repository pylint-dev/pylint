try:
    save_config(data)
except OSError as err:
    raise ConfigError(
        f"Failed to save config: {err}"
    ) from err  # [redundant-exception-message]
