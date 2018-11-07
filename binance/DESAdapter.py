#!/usr/bin/env	python 
# _*_ coding:utf-8 _*_
import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
#from urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

    # py3.4 default
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)


class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def create_ssl_context(self):
        #ctx = create_urllib3_context(ciphers=FORCED_CIPHERS)
        ctx = ssl.create_default_context()
        # allow TLS 1.0 and TLS 1.2 and later (disable SSLv3 and SSLv2)
        #ctx.options |= ssl.OP_NO_SSLv2
        #ctx.options |= ssl.OP_NO_SSLv3
        #ctx.options |= ssl.OP_NO_TLSv1
        ctx.options |= ssl.OP_NO_TLSv1_2
        ctx.options |= ssl.OP_NO_TLSv1_1
        #ctx.options |= ssl.OP_NO_TLSv1_3
        ctx.set_ciphers( CIPHERS )
        #ctx.set_alpn_protocols(['http/1.1', 'spdy/2'])
        return ctx

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = self.create_ssl_context()
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = self.create_ssl_context()
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)
