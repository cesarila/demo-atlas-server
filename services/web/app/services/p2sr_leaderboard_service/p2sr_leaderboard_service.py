import requests
from flask import jsonify
from . import p2sr_response

def get_display_name(steam_id=-1):
    if steam_id>=0:
        request_url = 'https://board.portal2.sr/profile/{steam_id}/json'.format(steam_id=steam_id)
        response = requests.get(request_url).json()['userData']
        try:
            response = requests.get(request_url)
        except:
            return p2sr_response.bad_gateway()
        if response.ok:
            profile_json = response.json()
            try:
                display_name = profile_json['userData']['displayName']
                return p2sr_response.success(display_name)
            except:
                return p2sr_response.not_found(steam_id)
        else:
            return p2sr_response.internal_server_error()
