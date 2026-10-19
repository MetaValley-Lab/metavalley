from fastapi import Request
from slowapi import Limiter


def get_real_client_ip(request: Request):
    """
    Recupera o ID real do cliente que foi enviado por proxy (Vercel).
    O cabeçaho 'X-Forwarded-For' contém a lista de IPs.
    O primeiro da lista é sempre o IP real do usuário. 
    """
    
    # 1. Verifica se o cabeçalho X-Forwarded-For existe
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        real_ip = x_forwarded_for.split(",")[0].strip()
        return real_ip
    
    # 2. Caso não encontre o primeiro cabeçalho, tenta com X-Real-IP
    x_real_ip = request.headers.get("x-real-ip")
    if x_real_ip:
        return x_real_ip
    
    # 3. Fallback: Se não houver proxy (ex: rodando localmente), usa host padrão
    if request.client and request.client.host:
        return request.client.host
    
    
    return "127.0.0.1"



limiter = Limiter(key_func=get_real_client_ip)

