import polyline
from flask import Blueprint, send_file


bp = Blueprint('export', __name__, url_prefix='/export')

@bp.route('/tar', methods=['GET'])
def export_tar():
    return send_file("../instance/tourloop-database.tar.gz")
