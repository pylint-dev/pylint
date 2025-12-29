try:
    save_config(data)
except OSError as err:
    raise ConfigError("Failed to save configuration") from err