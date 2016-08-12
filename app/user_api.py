# -*- coding: utf-8 -*-

# @date 2016/06/4
# @author yaoelvon@gmail.com
# @desc user api
# @record
#

import json
from flask import Blueprint, Response, request, current_app, jsonify
from app.models import User
from app.tenant import TenantContext
from app.database import db

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
    u = User.query.first()

    return jsonify({"user": u.name})


@user.route("/users", methods=["POST"])
def create_user():
    tenant = request.environ.get('tenant_ctx')
    u = User(tenant=tenant)
    u.name = "li"

    db.session.add(u)
    db.session.commit()

    print "user.company_id: {0}".format(u.company_id)

    return jsonify({"result": u.company_id})
