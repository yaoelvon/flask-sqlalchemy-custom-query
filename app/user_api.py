# -*- coding: utf-8 -*-

# @date 2016/06/4
# @author fengyao.me
# @desc user api
# @record
#

from flask import Blueprint, Response, request, current_app, jsonify
from app.models import User
from app.tenant import TenantContext

user = Blueprint('user', __name__)


@user.before_app_request
def filter_base_get():
    # 前端发送一个db_filters={"name":"vwms"}字典，将其存入租户实例
    tenant_ctx = TenantContext(request.args.get('db_filters'))
    print("tenant_ctx: {0}, type: {1}".format(tenant_ctx, type(tenant_ctx)))
    request.environ['tenant_ctx'] = tenant_ctx


@user.route("/users", methods=["GET"])
def users_get():
    users = User.query.all()

    return jsonify({"user": str(len(users))})


@user.route("/user", methods=["GET"])
def user_get():
    user = User.query.first()

    return jsonify({"user": user.name})
