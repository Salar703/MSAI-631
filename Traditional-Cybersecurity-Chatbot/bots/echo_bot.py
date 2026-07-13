# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self,
        members_added: List[ChannelAccount],
        turn_context: TurnContext,
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Hello! Welcome to the Cybersecurity Assistant. "
                        "Type 'help' to see my capabilities."
                    )
                )

    async def on_message_activity(self, turn_context: TurnContext):
        user_message = (turn_context.activity.text or "").lower().strip()

        if not user_message:
            response = (
                "I did not receive a valid message. "
                "Type 'help' to see my available commands."
            )

        elif user_message in ["hello", "hi", "hey"]:
            response = (
                "Hello! Welcome to the Cybersecurity Assistant. "
                "Type 'help' to see my available commands."
            )

        elif user_message in ["help", "commands"]:
            response = (
                "I can help you with the following topics:\n\n"
                "- password\n"
                "- phishing\n"
                "- mfa\n"
                "- controls\n"
                "- incident\n"
                "- capabilities\n"
                "- bye"
            )

        elif user_message == "capabilities":
            response = (
                "My capabilities include:\n\n"
                "- Password security guidance\n"
                "- Phishing awareness\n"
                "- Multi-factor authentication guidance\n"
                "- Basic security control information\n"
                "- Cybersecurity incident reporting guidance"
            )

        elif "password" in user_message:
            response = (
                "Use a strong and unique password or passphrase with at least "
                "12 characters. Do not reuse passwords, and consider using a "
                "password manager."
            )

        elif "phishing" in user_message:
            response = (
                "Be cautious with unexpected emails, links, attachments, and "
                "urgent requests. Verify the sender before clicking or responding."
            )

        elif (
            "mfa" in user_message
            or "multi-factor" in user_message
            or "multifactor" in user_message
        ):
            response = (
                "Multi-factor authentication adds another layer of security "
                "beyond a password. Use an authenticator application or security "
                "key when available."
            )

        elif "control" in user_message or "nist" in user_message:
            response = (
                "Security controls are safeguards used to protect systems and "
                "information. Examples include access control, audit logging, "
                "configuration management, encryption, and monitoring."
            )

        elif "incident" in user_message or "report" in user_message:
            response = (
                "Report suspected cybersecurity incidents immediately through "
                "your organization's approved reporting process. Preserve relevant "
                "details and avoid changing possible evidence."
            )

        elif user_message in ["bye", "goodbye", "exit", "quit"]:
            response = "Goodbye! Thank you for using the Cybersecurity Assistant."

        else:
            response = (
                "Sorry, I do not understand that request. "
                "Type 'help' to see my available commands."
            )

        await turn_context.send_activity(MessageFactory.text(response))