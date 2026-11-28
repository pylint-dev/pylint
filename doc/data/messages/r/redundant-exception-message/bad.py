try:
    save_config(data)
except OSError as err:
    raise ConfigError(f"Error: {err}") from err  # [redundant-exception-message]
