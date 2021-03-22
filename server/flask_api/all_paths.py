import polyline
from flask import Blueprint


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
