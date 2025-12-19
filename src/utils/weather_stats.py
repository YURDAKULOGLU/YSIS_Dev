class TemperatureProcessor:
    def __init__(self, temperatures: list):
        self.temperatures = temperatures

    def get_average(self) -> float:
        if not self.temperatures:
            raise ValueError("Temperature list is empty")
        return sum(self.temperatures) / len(self.temperatures)

    def get_extremes(self) -> tuple:
        if not self.temperatures:
            raise ValueError("Temperature list is empty")
        return min(self.temperatures), max(self.temperatures)
