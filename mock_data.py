# Mock Data - USE THIS PARAMETERS IN THE FRONTEND AND BACKEND ACCORDINGLY

import os

LINKED_IN_DATA = {
    'client_id': 'linkedin-client-id',
    'client_secret': 'linkedin-secret',
    'response_type': 'code',
    'auth_code': 'mock_auth_code_for_linked_in',
    'grant_type': 'authorization_code',
    'secret_key': os.getenv("REACT_JWT_SIGNING_KEY"),
    'jwt_expiration': 3600
}

FUSION_AUTH_DATA = {
    'client_id': 'fusionauth-client-id',
    'client_secret': 'fusionauth-secret',
    'response_type': 'code',
    'tenant_id': 'f82aa83e-a48c-4621-ab4c-ea2a1b7a5195',
    'auth_code': 'mock_auth_code_for_fusion_auth',
    'grant_type': 'authorization_code',
    'secret_key': os.getenv("RAILS_JWT_SIGNING_KEY"),
    'jwt_expiration': 3600
}