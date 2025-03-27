import logging

logger = logging.getLogger(__name__)

a = 5
b = 3
c = a + b
print(f"{a} +  {b} is {c}")

logger.info("Exitting")
