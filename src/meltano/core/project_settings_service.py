from meltano.core.settings_service import SettingsService


class ProjectSettingsService(SettingsService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._definitions = self.discovery_service.discovery.settings

    _env_namespace = "meltano"
    _db_namespace = "meltano"

    @property
    def _current_config(self):
        return self.config_service.current_config

    def _update_config(self):
        self.config_service.update_config()
