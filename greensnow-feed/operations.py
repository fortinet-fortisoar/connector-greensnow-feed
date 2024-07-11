"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import requests
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('greensnow-feed')


class GreenSnowFeed(object):
    def __init__(self, config, *args, **kwargs):
        self.url = config.get('server_url').strip('/')
        self.verify_ssl = config.get('verify_ssl')

    def make_rest_call(self, url, method, data=None, params=None):
        try:
            url = self.url
            response = requests.request(method, url, data=data, params=params, verify=self.verify_ssl,
                                        timeout=60)
            if response.ok:
                return response.text
            else:
                logger.error("{0}".format(response.status_code))
                raise ConnectorError("{0}:{1}".format(response.status_code, response.text))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def get_indicators(config, params):
    try:
        gs = GreenSnowFeed(config)
        endpoint = ''
        response = gs.make_rest_call(endpoint, 'GET')
        if response:
            response = response.split("\n")[:-1]
        return response
    except Exception as err:
        raise ConnectorError(str(err))


def check_health(config):
    try:
        response = get_indicators(config, params={})
        if response:
            return True
    except Exception as err:
        logger.info(str(err))
        raise ConnectorError(str(err))


operations = {
    'get_indicators': get_indicators
}
