# MIT License
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished 
# to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import requests
import common
from datetime import datetime

class APIAuthException(Exception):
    """Base class for other exceptions"""
    pass

def getServerStatus(access_token):
    apiPath = 'https://api.nitrado.net/services/%s/gameservers' % (common.game_server_id)

    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    # Get the Charging Status
    r = requests.get(apiPath, headers=headers)

    # Check the response and continue
    if r.status_code == 200: 
        return r.json()
    else:
        if r.status_code == 401:
            raise APIAuthException('Failed to fetch status, Authentication: ' + str(r.status_code) + ' ' + r.reason)
        elif r.status_code == 429:
            raise Exception('Failed to fetch status, the rate limit has been exceeded: ' + str(r.status_code) + ' ' + r.reason)
        elif r.status_code == 503:
            raise Exception('Failed to fetch status, maintenance. API is currently not available: ' + str(r.status_code) + ' ' + r.reason)
        else:
            raise Exception('Failed to fetch status, unable to proceed: ' + str(r.status_code) + ' ' + r.reason)

def restartServer(access_token):
    apiPath = 'https://api.nitrado.net/services/%s/gameservers/restart' % (common.game_server_id)

    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + access_token
    }

    # Send the request
    r = requests.post(apiPath, headers=headers)

    # Check the response and continue
    if r.status_code == 200: 
        status = r.json()['status']
        message = r.json()['message']
        return '%s %s' %(status, message)
    else:
        if r.status_code == 401:
            raise APIAuthException('Failed to start service, Authentication: ' + str(r.status_code) + ' ' + r.reason)
        elif r.status_code == 429:
            raise Exception('Failed to start service, the rate limit has been exceeded: ' + str(r.status_code) + ' ' + r.reason)
        elif r.status_code == 503:
            raise Exception('Failed to start service, maintenance. API is currently not available: ' + str(r.status_code) + ' ' + r.reason)
        else:
            raise Exception('Failed to start service, unable to proceed: ' + str(r.status_code) + ' ' + r.reason)

try:
    data = getServerStatus(common.nitrado_access_token)
    # Avaiable status'  = restarting|started|stopping|stopped
    status = data['data']['gameserver']['status']
    if status == 'stopped':
        common.log('Game Service is stopped, sending start request.')
        response = restartServer(common.nitrado_access_token)
        common.log(response)
    else:
        common.log('Game Service Status is: %s' % (status))
except APIAuthException as e:
    common.log(str(e))
except Exception as e:
    common.log(str(e))
