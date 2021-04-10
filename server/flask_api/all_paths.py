import polyline
from flask import Blueprint, request, send_file
from algo_3 import Algo3
from algo_2 import Algo2
from algo_1 import Algo1
from path_options import PathOptions

from flask_api.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('sample', methods=['GET'])
def sample():

    paths = {"paths": []}
    paths["paths"].append(polyline.encode([(53.513998, -113.523167), (53.523108, -113.501408),
                                           (53.536034, -113.484126), (53.547834, -113.504223), (53.560935, -113.503168)], 6))

    paths["paths"].append(polyline.encode(
        [(53.522907, -113.620026), (53.534730, -113.589917), (53.558614, -113.584600)], 6))
    return paths


@bp.route('alldirtpaths', methods=['GET'])
def all_paths():
    return send_file("../instance/all_dirt_paths.txt")


@bp.route('allbikepaths', methods=['GET'])
def all_bike_paths():
    return send_file("../instance/all_bike_paths.txt")


@bp.route('', methods=['GET', 'POST'])
def demo_pins():
    if request.method == 'POST':
        path_options = PathOptions()
        err = path_options.setOptionsJson(request)
        if err:
            return {"errMessage": err}

        if path_options.getAlgorithmType() == 'algo1':
            print('Running Algorithm 1')
            algo = Algo1(path_options, get_db())
        elif path_options.getAlgorithmType() == 'algo2':
            print('Running Algorithm 2')
            algo = Algo2(path_options, get_db())
        elif path_options.getAlgorithmType() == 'algo3':
            print('Running Algorithm 3')
            algo = Algo3(path_options, get_db())
        else:
            return {"errMessage": "Invalid algorithm type."}

        algo.generateRoutes()
        return algo.getRoutesJson()


# http://localhost:5000/api/closest_point?lat=%2253.509905%22&lon=%22-113.541233%22
# return {"lat":53.5714699,"lon":-113.6278968}
@bp.route('closest_point', methods=['GET'])
def get_closest_point():
    db = get_db()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return db.getClosestPoint(lat, lon)


@bp.route('closest_point_to_path', methods=['GET'])
def get_closest_point_path():
    db = get_db()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pathtype = request.args.get('pathtype')
    return db.getClosestPointToPathtype(pathyype, lat, lon)
