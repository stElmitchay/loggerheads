"""
Discord webhook integration for sending daily summaries.
"""

import requests
import json
from datetime import datetime


def send_to_discord(webhook_url, summary_text):
    """
    Send the daily summary to Discord via webhook.

    Args:
        webhook_url (str): Discord webhook URL
        summary_text (str): Formatted summary text

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not webhook_url:
        print("❌ Discord webhook URL not configured")
        return False

    try:
        # Discord has a 2000 character limit per message
        # Split into multiple messages if needed
        max_length = 2000
        messages = []

        if len(summary_text) <= max_length:
            messages.append(summary_text)
        else:
            # Split by sections to keep formatting intact
            sections = summary_text.split('\n\n')
            current_message = ""

            for section in sections:
                if len(current_message) + len(section) + 2 <= max_length:
                    current_message += section + "\n\n"
                else:
                    if current_message:
                        messages.append(current_message.strip())
                    current_message = section + "\n\n"

            if current_message:
                messages.append(current_message.strip())

        # Send each message
        for i, message in enumerate(messages):
            payload = {
                "content": message,
                "username": "Daily Work Tracker"
            }

            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code != 204:
                print(f"❌ Failed to send Discord message {i+1}/{len(messages)}: {response.status_code}")
                return False

            # Discord rate limit: wait a bit between messages
            if i < len(messages) - 1:
                import time
                time.sleep(1)

        print(f"✅ Summary sent to Discord ({len(messages)} message(s))")
        return True

    except Exception as e:
        print(f"❌ Error sending to Discord: {e}")
        return False


def format_for_discord(summary_text):
    """
    Format the summary text for Discord (add code blocks for better readability).

    Args:
        summary_text (str): Plain text summary

    Returns:
        str: Discord-formatted summary
    """
    # Add header with current date
    date_str = datetime.now().strftime("%B %d, %Y")

    formatted = f"**📅 Daily Work Summary - {date_str}**\n\n"
    formatted += "```\n"
    formatted += summary_text
    formatted += "\n```"

    return formatted


def send_summary_to_discord(webhook_url, summary_text, use_formatting=True):
    """
    Send formatted daily summary to Discord.

    Args:
        webhook_url (str): Discord webhook URL
        summary_text (str): Summary text to send
        use_formatting (bool): Whether to add Discord code block formatting

    Returns:
        bool: True if sent successfully
    """
    if use_formatting:
        formatted_text = format_for_discord(summary_text)
    else:
        formatted_text = summary_text

    return send_to_discord(webhook_url, formatted_text)
