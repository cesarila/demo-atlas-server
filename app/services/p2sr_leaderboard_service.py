import requests

def get_display_name(steam_id=-1):
    if steam_id>=0:
        request_url = 'https://board.portal2.sr/profile/{steam_id}/json'.format(steam_id=steam_id)
        response = requests.get(request_url).json()['userData']
        if response:
            return response['displayName']
        else:
            return None