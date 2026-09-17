# ötlet 60 másodperceként 10 darab requestet küldhet egy darab ip-cím
# Ehhez emlékezdni kell, hogy az adott ip cím mikor küdöt, és mennyit
# ezt egy lista mondja majd meg

from collections import defaultdict
"""
Normális Dict[] ha csak simán lekérek valamit ami nincsen benne, akkor KeyErrort ad
A defaultdict viszont, ad neki egy alapértékét, ha nincsen benne

requests["192.168.1.5"] -> ehhez rak egy alapértéket
"""
from time import time
# itt pedig az időt adja vissza, ilyen uxit formátumban, nem baj, hogy nem értjük, számolni tudjunk vele

from fastapi import HTTPException, Request

# azért kell a Request mert tartalmazza az aktuális HTTP request információit pl.: klines IP, HTTP method, URL, stb

MAX_REQUESTS = 10
WINDOW = 60
    
# ez közös, tehát Mind én, mint Béla egy közös Default Dictből hívjuk le, csak más az ip_címünk
requests_history = defaultdict(list)

"""
E miatt, ha azt mondom, hogy: 
requests["192.168.1.5"].append(123456789)

akkor ->
{
    "192.168.1.5": [123456789]
}

és ha tovább pakolok bele, akkor ez fog gyűlni.
és azért lista, mert több időt is kell egy ip-hez tárolni
"""
def rate_limit(request: Request):
    
    current_time = time()
    client_ip = request.client.host

    # Csak azokat tartjuk meg, amik a 60 másodpercnél(1 percnél) kisebbek
    requests_history[client_ip] = [
        timestamp
        for timestamp in requests_history[client_ip]
        if current_time - timestamp < WINDOW
    ]

    # megnézzük, hogy a hossza, tehát 60 másodpercben benne lévők, de a maximális hívásnál túl léptek-e
    if len(requests_history[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
    
    # hozzá tesszük a meglévő hivásokhoz
    requests_history[client_ip].append(current_time)