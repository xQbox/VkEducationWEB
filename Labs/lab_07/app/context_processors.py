from django.conf import settings 
import jwt
import time
from askme_rodinkov.settings import CENTRIFUGO_SECRET_KEY, CENTRIFUGO_WS_URL

def get_centrifugo_info(request):
    secret = CENTRIFUGO_SECRET_KEY
    user_id = str(request.user.id) if request.user.is_authenticated else "anonymous"
    claims = {"sub": user_id, "exp": int(time.time()) + 3600}
    
    token = jwt.encode(claims, secret, algorithm="HS256")
    
    return {"token": token, "ws_url": CENTRIFUGO_WS_URL}
