class DataUpdateCoordinator:
    def __init__(self, hass, logger, name, update_interval=None, update_method=None):
        self.hass = hass
        self.logger = logger
        self.name = name
        self.update_interval = update_interval
        self.data = None

    def __class_getitem__(cls, key):
        return cls

class UpdateFailed(Exception):
    pass
