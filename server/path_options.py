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

    def __init__(self, start=(0.0, 0.0) , end=(0.0, 0.0), path_pref="", target_d=0.0, algo_string=""):
        self._start_lat_long = start
        self._end_lat_long = end
        self._path_pref = path_pref
        self._target_distance = target_d
        self._algorithm_type = algo_string

    # getters

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


    # setters

    def setOptions(self, start, end, path_pref, target_d, algo_string):
        self._start_lat_long = start
        self._end_lat_long = end
        self._path_pref = path_pref
        self._target_distance = target_d
        self._algorithm_type = algo_string
        return

    def setOptionsLoop(self, start, path_pref, target_d, algo_string):
        self.setOptions(start, start, path_pref, target_d, algo_string)
        return

    def setOptionsJson(self, json_object):
        # TODO: set self from json_object
        return

