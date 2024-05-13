from data_handler.thinkfolio_position_handler import ThinkfolioPositionHandler


class GuiModel:
    default_config_file = 'configuration_file.json'

    def __init__(self):
        self.position_handler = ThinkfolioPositionHandler()

    def get_target_positions(self, date=None):
        output = self.position_handler.get_position(date)
        return output
