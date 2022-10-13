import asyncio
import json
from logging import getLogger
import sys

from .node import get_order
from .. import __identifier__


logger = getLogger(f"{__identifier__}.get_order")

try:
    message = json.loads(sys.argv[1])
except IndexError:
    raise ValueError("missing required `message` argument") from None

try:
    context = json.loads(sys.argv[2])
except IndexError:
    raise ValueError("missing `context` argument") from None

output = asyncio.run(get_order(message, context))

if output is None:
    logger.error("Received null output.")
    sys.exit(1)

print(json.dumps(output))
