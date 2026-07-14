# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from typing import Any

from aiohttp import web
from aiohttp.web import Request, Response
try:
    from azure.ai.textanalytics import TextAnalyticsClient
except ImportError:  # pragma: no cover
    TextAnalyticsClient = Any  # type: ignore[assignment]
from azure.core.credentials import AzureKeyCredential
from botbuilder.core import TurnContext
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botbuilder.schema import Activity, ActivityTypes

from bots import EchoBot
from config import DefaultConfig


CONFIG = DefaultConfig()


def create_text_analytics_client() -> TextAnalyticsClient:
    """
    Create the Azure AI Language client used for sentiment analysis.
    """

    if not CONFIG.AZURE_LANGUAGE_ENDPOINT:
        raise ValueError(
            "AZURE_LANGUAGE_ENDPOINT is missing. "
            "Set it in the VS Code PowerShell terminal."
        )

    if not CONFIG.AZURE_LANGUAGE_KEY:
        raise ValueError(
            "AZURE_LANGUAGE_KEY is missing. "
            "Set it in the VS Code PowerShell terminal."
        )

    credential = AzureKeyCredential(CONFIG.AZURE_LANGUAGE_KEY)

    return TextAnalyticsClient(
        endpoint=CONFIG.AZURE_LANGUAGE_ENDPOINT,
        credential=credential,
    )


# Create the Bot Framework adapter.
ADAPTER = CloudAdapter(
    ConfigurationBotFrameworkAuthentication(CONFIG)
)


# Catch-all error handler.
async def on_error(context: TurnContext, error: Exception):
    print(
        f"\n[on_turn_error] Unhandled error: {error}",
        file=sys.stderr,
    )
    traceback.print_exc()

    await context.send_activity(
        "The bot encountered an error while processing your message."
    )
    await context.send_activity(
        "Please check the VS Code terminal for more information."
    )

    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )

        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error


# Create the Azure AI Language client.
TEXT_ANALYTICS_CLIENT = create_text_analytics_client()


# Create the cybersecurity chatbot and give it access to Azure AI.
BOT = EchoBot(TEXT_ANALYTICS_CLIENT)


# Listen for incoming requests at /api/messages.
async def messages(req: Request) -> Response:
    return await ADAPTER.process(req, BOT)


APP = web.Application(
    middlewares=[aiohttp_error_middleware]
)

APP.router.add_post("/api/messages", messages)


if __name__ == "__main__":
    try:
        print("Cybersecurity chatbot is starting.")
        print("Azure AI Language connection is configured.")
        print(f"Listening on http://localhost:{CONFIG.PORT}")

        web.run_app(
            APP,
            host="localhost",
            port=CONFIG.PORT,
        )

    except Exception as error:
        print(f"Startup error: {error}", file=sys.stderr)
        raise