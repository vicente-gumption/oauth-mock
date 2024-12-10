import logging
import time
import jwt
import datetime
from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS

from mock_data import FUSION_AUTH_DATA, LINKED_IN_DATA

"""
app.py

This is a simulator for local development and testing. This implements the following services:

* LinkedIn OAuth API (https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?tabs=HTTPS1)
* FusionAuth OAuth API

Please note that the real instances also validate the redirect_uri, this simulator does not.

"""

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

app = Flask(__name__)
CORS(app)

@app.route('/linkedin/authorization', methods=['GET', 'POST'])
def li_authorization():
    """
    The endpoint matches the naming of the real LinkedIn API
    """

    if request.method == 'GET':
        args = request.args.to_dict()
    else:
        args = request.form.to_dict()
    logger.info("Authorization: %s", args)

    response_type = args.get('response_type')
    client_id = args.get('client_id')
    redirect_uri = args.get('redirect_uri')
    state = args.get('state')
    scope = args.get('scope')

    if redirect_uri is None or redirect_uri == '':
        return "No redirect URI passed in request", 400

    result_url = redirect_uri
    result_url += f"?state={state}"

    if request.method == 'POST':
        approved = args.get('approve')
        if approved == "yes":
            result_url += f"&code={LINKED_IN_DATA['auth_code']}"
        else:
            result_url += f"&error=user_cancelled_authorize&error_description=User%20said%20NO"

        return redirect(result_url)
    
    if client_id == LINKED_IN_DATA['client_id'] \
        and response_type == LINKED_IN_DATA['response_type']:
        return render_template("authorize.html", client_id=client_id, service_name="LinkedIn", service_path="/linkedin/authorization")
    
    result_url += f"&error=user_cancelled_authorize&error_description=invalid%20request%20params"

    if state is not None and state != '':
        result_url += f"&state={state}"
    return redirect(result_url)


@app.route('/fusionauth/authorize')
def fa_authorize():
    """
    The endpoint matches the naming of the real FusionAuth AIP
    """
    logger.info("Authorization: %s", request.args.to_dict())
    time.sleep(3)
    response_type = request.args.get('response_type')
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    tenant_id = request.args.get('tenantId')
    state = request.args.get('state')
    scope = request.args.get('scope')

    if redirect_uri is None or redirect_uri == '':
        return "No redirect URI passed in request", 400

    result_url = redirect_uri
    if client_id == FUSION_AUTH_DATA['client_id']               \
        and response_type == FUSION_AUTH_DATA['response_type']  \
        and tenant_id == FUSION_AUTH_DATA['tenant_id']:
        # Simulate user authorization by redirecting with an auth code
        result_url += f"?code={FUSION_AUTH_DATA['auth_code']}&locale=en&userState=Authenticated"
    else:
        result_url += f"?error=user_cancelled_authorize&error_description=invalid%20request%20params"
    
    if state is not None and state != '':
        result_url += f"&state={state}"
    return redirect(result_url)


@app.route('/linkedin/accessToken', methods=['POST'])
def li_accessToken():
    logger.info("LinkedIn Token Exchange: %s", request.form.to_dict())
    time.sleep(3)
    grant_type = request.form.get('grant_type')
    auth_code = request.form.get('code')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    state = request.form.get('state')
    redirect_uri = request.form.get('redirect_uri')
    if redirect_uri is not None and redirect_uri != '' \
        and grant_type == LINKED_IN_DATA['grant_type'] \
        and auth_code == LINKED_IN_DATA['auth_code']   \
        and client_id == LINKED_IN_DATA['client_id']   \
        and client_secret == LINKED_IN_DATA['client_secret']:
        payload = {
            "sub": "123",
            "iat": datetime.datetime.now(datetime.UTC),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=LINKED_IN_DATA['jwt_expiration'])
        }
        access_token = jwt.encode(payload, LINKED_IN_DATA['secret_key'], algorithm='HS256')
        logger.info(f"Token: {access_token}")
        return jsonify({
            "access_token": access_token,
            "expires_in": LINKED_IN_DATA['jwt_expiration'],
            "refresh_token": "REFRESH_TOKEN",
            "refresh_token_expires_in": 64000,
            "scope": "",
            "state": state
        })
    return jsonify({"error": "invalid request params"}), 401


@app.route('/fusionauth/accessToken', methods=['POST'])
def fa_accessToken():
    logger.info("LinkedIn Token Exchange: %s", request.form.to_dict())
    time.sleep(3)
    grant_type = request.form.get('grant_type')
    auth_code = request.form.get('code')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    redirect_uri = request.form.get('redirect_uri')
    if redirect_uri is not None and redirect_uri != ''  \
        and grant_type == FUSION_AUTH_DATA['grant_type']\
        and auth_code == FUSION_AUTH_DATA['auth_code']  \
        and client_id == FUSION_AUTH_DATA['client_id']  \
        and client_secret == FUSION_AUTH_DATA['client_secret']:
        return jsonify({
            "access_token": 'd31f9c37-2df6-4b2c-abf0-0bfc724394bd',
            "expires_in": 64000,
            "id_token": '2ade66ba-0683-4be9-8563-b53eda883586',
            "refresh_token": "REFRESH_TOKEN",
            "refresh_token_expires_in": 64000,
            "token_type": "Bearer",
            "scope": "openid offline_access"
        })
    return jsonify({"error": "invalid request params"}), 401


@app.route('/linkedin/me')
def user_info():
    access_token = request.headers.get('Authorization', '').split(' ')[-1]
    if access_token == ACCESS_TOKEN:
        return jsonify(USER_INFO)
    return "Invalid or missing token", 401


if __name__ == '__main__':
    app.run(debug=True, port=15000)
