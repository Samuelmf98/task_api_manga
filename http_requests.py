'''Esta función sirve para no tener problemas de timeout o de sesión finalizada'''
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from aiohttp import ClientSession


async def aiohttp_retry_session():
    retry_options = ExponentialRetry(attempts=3)
    # Asegúrate de retornar el contexto de RetryClient
    return aiohttp.ClientSession()