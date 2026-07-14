# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os


class DefaultConfig:
    """Bot and Azure AI configuration."""

    PORT = 3978

    # Microsoft Bot Framework credentials.
    # These can remain blank when testing locally in Bot Framework Emulator.
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # Azure AI Language service configuration.
    AZURE_LANGUAGE_ENDPOINT = os.environ.get(
        "AZURE_LANGUAGE_ENDPOINT",
        ""
    )

    AZURE_LANGUAGE_KEY = os.environ.get(
        "AZURE_LANGUAGE_KEY",
        ""
    )