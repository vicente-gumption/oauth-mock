import jwt
import datetime
import sys

from mock_data import FUSION_AUTH_DATA, LINKED_IN_DATA


def linkedin_token():
    if LINKED_IN_DATA['secret_key'] is None or len(LINKED_IN_DATA['secret_key'].strip()) == 0:
        raise "LinkedIn secret key not defined in environment"

    payload = {
        "sub": "123",
        "iat": datetime.datetime.now(datetime.UTC),
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=LINKED_IN_DATA['jwt_expiration'])
    }
    return jwt.encode(payload, LINKED_IN_DATA['secret_key'], algorithm='HS256')


def fusionauth_token():
    if FUSION_AUTH_DATA['secret_key'] is None or len(FUSION_AUTH_DATA['secret_key'].strip()) == 0:
        raise "FusionAuth secret key not defined in environment"
    payload = {
        "applicationId": "469b0ba1-a849-4603-883e-3b05c0d2b7ce",
        "aud": "469b0ba1-a849-4603-883e-3b05c0d2b7ce",
        "authenticationType": "PASSWORD",
        "email": "user@fusionauth.io",
        "iat": datetime.datetime.now(datetime.UTC),
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=FUSION_AUTH_DATA['jwt_expiration']),
        "iss": "gumption.com",
        "sub": "6558c73f-b345-4917-9aac-0feab21eeeeb"
    }
    return jwt.encode(payload, FUSION_AUTH_DATA['secret_key'], algorithm='HS256')


def usage():
    print("Usage: python token.py <type>")
    print("  where <type> is one of: 'linkedin' or 'fusionauth'")
    print("Example: python token.py fusionauth")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)
    elif sys.argv[1].strip().lower() == 'linkedin':
        print("LinkedIn Token:")
        print(linkedin_token())
    elif sys.argv[1].strip().lower() == 'fusionauth':
        print("Fusion Auth Token:")
        print(fusionauth_token())
    else:
        usage()
        sys.exit(-1)

