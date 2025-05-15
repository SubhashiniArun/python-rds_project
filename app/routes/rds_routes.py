from flask import Blueprint, jsonify

from ..utils.rds_instance_connection import create_rds_connection

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route("/test_rds_connection", methods=['GET'])
def test_rds_connection():
    create_rds_connection()
    return jsonify(message="RDS Connection!")
