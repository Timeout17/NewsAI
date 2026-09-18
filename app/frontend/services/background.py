"""
Azért kell, hogy az adott függvényt, egy másik szálon futtasuk 
ThreadPoolExecutor ez való erre
"""

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)



