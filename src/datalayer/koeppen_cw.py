from datalayers.datasources.koeppen_layer import KoeppenLayer


class KoeppenCw(KoeppenLayer):
    def __init__(self) -> None:
        super().__init__()

        self.climate_types = [
            self.ClimateTypes.Cwa,
            self.ClimateTypes.Cwb,
            self.ClimateTypes.Cwc,
        ]
