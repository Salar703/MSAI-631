# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from azure.ai.textanalytics import TextAnalyticsClient
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    def __init__(self, text_analytics_client: TextAnalyticsClient):
        self.text_analytics_client = text_analytics_client

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
                        "I can answer basic cybersecurity questions and analyze "
                        "the sentiment of your message using Azure AI Language. "
                        "Type 'help' to see my capabilities."
                    )
                )

    async def on_message_activity(self, turn_context: TurnContext):
        original_message = (turn_context.activity.text or "").strip()
        user_message = original_message.lower()

        if not original_message:
            await turn_context.send_activity(
                MessageFactory.text(
                    "I did not receive a valid message. "
                    "Type 'help' to see my available commands."
                )
            )
            return

        sentiment_message = self.get_sentiment_message(original_message)

        if user_message in ["hello", "hi", "hey"]:
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
                "- sentiment\n"
                "- bye"
            )

        elif user_message == "capabilities":
            response = (
                "My capabilities include:\n\n"
                "- Password security guidance\n"
                "- Phishing awareness\n"
                "- Multi-factor authentication guidance\n"
                "- Basic security control information\n"
                "- Cybersecurity incident reporting guidance\n"
                "- Sentiment analysis using Azure AI Language"
            )

        elif user_message == "sentiment":
            response = (
                "I use Azure AI Language to analyze whether your message is "
                "positive, neutral, negative, or mixed."
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
            response = (
                "Goodbye! Thank you for using the Cybersecurity Assistant."
            )

        else:
            if "Positive" in sentiment_message:
                response = (
                    "I'm glad you're interested in cybersecurity!\n\n"
                    "Type 'help' to explore the topics I can assist you with."
                )

            elif "Negative" in sentiment_message:
                response = (
                    "Cybersecurity can sometimes feel challenging.\n\n"
                    "I'm here to explain concepts step by step. "
                    "Type 'help' to see the available topics."
                )

            else:
                response = (
                    "Thanks for your message.\n\n"
                    "Ask me a cybersecurity question or type 'help' "
                    "to see my capabilities."
                )

        final_response = f"{sentiment_message}\n\n{response}"

        await turn_context.send_activity(
            MessageFactory.text(final_response)
        )

    def get_sentiment_message(self, message: str) -> str:
        try:
            result = self.text_analytics_client.analyze_sentiment(
                documents=[message]
            )[0]

            if result.is_error:
                return (
                    "Azure AI sentiment analysis could not process "
                    "the message."
                )

            sentiment = result.sentiment.capitalize()
            scores = result.confidence_scores

            return (
                f"Azure AI Sentiment: {sentiment}\n"
                f"Positive: {scores.positive:.2f} | "
                f"Neutral: {scores.neutral:.2f} | "
                f"Negative: {scores.negative:.2f}"
            )

        except Exception as error:
            print(f"Azure AI sentiment analysis error: {error}")

            return (
                "Azure AI sentiment analysis is temporarily unavailable, "
                "but I can still answer cybersecurity questions."
            )