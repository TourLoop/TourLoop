import polyline
from flask import Blueprint, request
from flask_api import query_helpers


from flask_api.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('', methods=['GET'])
def all_paths():
    db = get_db()

    paths = {"paths": []}
    paths["paths"].append(polyline.encode([(53.513998, -113.523167), (53.523108, -113.501408),
                                           (53.536034, -113.484126), (53.547834, -113.504223), (53.560935, -113.503168)], 6))

    paths["paths"].append(polyline.encode(
        [(53.522907, -113.620026), (53.534730, -113.589917), (53.558614, -113.584600)], 6))
    return paths


# http://localhost:5000/api/closest_point?lat=%2253.509905%22&lon=%22-113.541233%22
# return {"lat":53.5714699,"lon":-113.6278968}
@bp.route('closest_point', methods=['GET'])
def get_closest_point():
    db = get_db()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return query_helpers.closest_point(db, lat, lon)

@bp.route('closest_point_to_path', methods=['GET'])
def get_closest_point_path():
    db = get_db()
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    pathtype = request.args.get('pathtype')
    return query_helpers.closest_point_to_pathtype(db, pathtype, lat, lon)
