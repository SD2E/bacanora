from agavepy.agave import Agave, AgaveError


class AgaveNonceOnly(Agave):
    """Special Agave client that streamlines use of an Abaco nonce"""
    UNAUTH_PARAMS = [('api_server', True, 'api_server', None),
                     ('nonce', True, 'nonce', None)]

    def __init__(self, **kwargs):
        for param, mandatory, attr, default in self.UNAUTH_PARAMS:
            try:
                value = (kwargs[param] if mandatory else kwargs.get(
                    param, default))
            except KeyError:
                raise AgaveError('parameter "{}" is mandatory'.format(param))
            setattr(self, attr, value)
        kwargs['use_nonce'] = True
        kwargs.pop('nonce')
        super(AgaveNonceOnly, self).__init__(**kwargs)


def with_refresh(client, f, *args, **kwargs):
    """Call function ``f`` and refresh token if needed."""
    try:
        if getattr(client, 'nonce', None) is not None:
            kwargs['nonce'] = getattr(client, 'nonce', None)
        return f(*args, **kwargs)
    except requests.exceptions.HTTPError as exc:
        try:
            # Old versions of APIM return errors in XML:
            code = ElementTree.fromstring(exc.response.text)[0].text
        except Exception:
            # Any error here means the response was not XML.
            try:
                # Try to see if it's a json response,
                exc_json = exc.response.json()
                # if so, check if it is an expired token error (new versions of APIM return JSON errors):
                if 'Invalid Credentials' in exc_json.get('fault').get(
                        'message'):
                    client.token.refresh()
                    return f(*args, **kwargs)
                #  otherwise, return the JSON
                return exc.response
            except Exception:
                # Re-raise it, as it's not an expired token
                raise exc
        # only catch 'token expired' exception
        # other codes may mean a different error
        if code not in ['900903', '900904']:
            raise
        client.token.refresh()
        return f(*args, **kwargs)
