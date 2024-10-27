from datalayers.datasources.copernicus_layer import CopernicusLayer

class CopernicusHerbwet(CopernicusLayer):

    def __init__(self):
        super().__init__()

        self.area_of_interest = [
            'herbaceous_wetland',
        ]
