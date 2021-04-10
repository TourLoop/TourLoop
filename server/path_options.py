class PathOptions:
    """
    >>> path_opts_1 = PathOptions()
    >>> path_opts_1.setOptionsLoop((0.0, 1.1), "bike", 2.2, "algo1")

    >>> path_opts_2 = PathOptions((0.0, 1.1), (0.0, 1.1), "bike", 2.2, "algo1")

    >>> path_opts_1.getStart() == path_opts_1.getEnd()
    True
    >>> path_opts_1.getStart() == path_opts_2.getStart()
    True
    """


    BIKE_PATH = "bike"
    DIRT_PATH = "dirt"
    PAVED_PATH = "paved"

    ALGO_1 = "algo1"
    ALGO_2 = "algo2"
    ALGO_3 = "algo3"

    def __init__(self, start=(0.0, 0.0) , end=(0.0, 0.0), path_pref="", target_d=0.0, algo_string=""):
        self._start_lat_long = start
        self._end_lat_long = end
        self._path_pref = path_pref
        self._target_distance = target_d
        self._algorithm_type = algo_string

    def getStart(self):
        return self._start_lat_long

    def getEnd(self):
        return self._end_lat_long

    def getPathType(self):
        return self._path_pref

    def getTargetDistance(self):
        return self._target_distance

    def getAlgorithmType(self):
        return self._algorithm_type

    def setOptionsJson(self, r):
        point_to_point = r.json['pointToPoint']
        start_location = r.json['startLocation']
        end_location = r.json['endLocation']
        target_distance = r.json['targetRouteDistance']
        path_type = r.json['pathType']
        algorithm = r.json['algorithm']

        start_lat_lng = start_location.split(",", 1)
        end_lat_lng = end_location.split(",", 1)

        try:
            float(target_distance) 
        except:
            return "Unable to parse target distance."

        if float(target_distance) <= 0.0 or float(target_distance) > 20.0:
            return "Target distance must be greater than 0.0 km and less than 20.0 km."

        try:
            float(start_lat_lng[0])
            float(start_lat_lng[1])
            float(end_lat_lng[0])
            float(end_lat_lng[1])
        except:
            return "Unable to parse the start or end location."

        if path_type not in set([PathOptions.BIKE_PATH, PathOptions.DIRT_PATH, PathOptions.PAVED_PATH]):
            return "Invalid path type."

        if algorithm not in set([PathOptions.ALGO_1, PathOptions.ALGO_2, PathOptions.ALGO_3]):
            return "Invalid algorithm type."

        self._start_lat_long = tuple(float(coord)
                              for coord in start_location.split(',', 1))
        self._end_lat_long = tuple(float(coord) for coord in end_location.split(','))
        self._path_pref = path_type
        self._target_distance = float(target_distance)
        self._algorithm_type = algorithm