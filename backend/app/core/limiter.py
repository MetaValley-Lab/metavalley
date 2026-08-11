# app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Define que o limite será calculado pelo endereço de IP remoto do cliente
limiter = Limiter(key_func=get_remote_address)