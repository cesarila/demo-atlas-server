from flask import jsonify

def success(display_name):
    response = jsonify({
        'displayName': display_name
        })
    response.status_code = 200
    return response

def not_found(steam_id=-1):
    response = jsonify({
        'error': 'not found',
        'message': ('The Steam id {} is not associated with a board.portal2.sr profile.').format(steam_id)
            })
    response.status_code = 404
    return response

def internal_server_error():
    response = jsonify({
        'error': 'internal server error',
        'message': 'board.portal2.sr made breaking changes to its API'
        })
    response.status_code = 500
    return response

def bad_gateway():
    response = jsonify({
        'error': 'bad gateway',
        'message': 'board.portal2.sr is not online or otherwise inaccessible'
        })
    response.status_code = 502
    return response