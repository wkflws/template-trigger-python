from typing import Any, Optional

from wkflws.events import Event
from wkflws.http import http_method, Request
from wkflws.triggers.webhook import WebhookTrigger

from . import __identifier__, __version__


async def process_webhook_request(request: Request) -> Optional[Event]:
    """Accept and process an HTTP request returning a event for the bus."""

    # Most webhooks include a header with a unique id that can be used as the event's
    # id. This would allow tracing back to the source.
    identifier = request.headers["remote-id"]

    # Most webhooks provide data as JSON so no transformations are needed. If they are
    # sending something other than JSON then you will need to format it as a JSON
    # serializable dict.
    data = json.loads(request.body)

    return Event(identifier, request.headers, data)


async def accept_event(event: Event) -> tuple[Optional[str], dict[str, Any]]::
    """Accept and process data from the event bus."""
    return "MODNAME.node", event.data


my_webhook_trigger = WebhookTrigger(
    client_identifier=__identifier__,
    client_version=__version__,
    process_func=accept_event,
    routes=(
        (
            (http_method.POST,),
            "/webhook/",
            process_webhook_request,
        ),
    ),
)
