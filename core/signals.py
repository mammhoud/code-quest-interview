
from cacheops.signals import cache_invalidated
from core import coreLogger as logger 

def log_invalidation(sender, **kwargs):
    logger.info(f"🔁 Cache invalidated for model: {sender.__name__}")


# Connect signal
cache_invalidated.connect(log_invalidation)
