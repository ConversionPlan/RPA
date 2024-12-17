import os
import json
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
channel_id = "C084F8LFU94"

client = WebClient(token=slack_bot_token)


def format_results():
    any_errors = False
    status_names = {
        "passed": ":white_check_mark: Passed",
        "failed": ":x: Failed",
        "skipped": ":ballot_box_with_check: Skipped",
    }

    today = datetime.now().strftime("%B %d, %Y")
    formatted_results = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":robot_face: RPA Bot Report :robot_face:",
            },
        },
        {
            "type": "context",
            "elements": [
                {"text": f"*{today}* | QA Team Automated Tests", "type": "mrkdwn"}
            ],
        },
    ]

    with open("./report/output/results.json", "r") as file:
        json_data = json.load(file)

    for feature in json_data:
        if feature["tags"][0] == "Ignore":
            continue
        formatted_results.append({"type": "divider"})
        formatted_results.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":teste: *{feature["name"].upper()}* :teste:",
                },
            }
        )

        for scenario in feature["elements"]:
            status = status_names[scenario["status"]]
            formatted_results.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{scenario["name"]}: {status}"},
                }
            )

            if scenario["status"] == "failed":
                any_errors = True
                for step in scenario["steps"]:
                    try:
                        if step["result"]["status"] == "failed":
                            formatted_results.append(
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"Step: {step["name"]}",
                                    },
                                }
                            )

                            error_message = "\n".join(step["result"]["error_message"])

                            formatted_results.append(
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": f"Error:\n```{error_message}```",
                                    },
                                }
                            )
                    except KeyError:
                        pass

    formatted_results.append({"type": "divider"})
    formatted_results.append({"type": "divider"})
    formatted_results.append(
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":robot_face: CONCLUSION :robot_face:",
            },
        }
    )

    if any_errors == True:
        formatted_results.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":alert: @here some errors were found! Take a look as soon as possible. :alert:\nReact with :eyes: once you are looking into it.",
                },
            }
        )
    else:
        formatted_results.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":tada: No errors were found! :tada:",
                },
            }
        )

    return formatted_results


def send_message():
    try:
        message = format_results()
        response = client.chat_postMessage(channel=channel_id, blocks=message)

        print("Message sent successfully!", response["ts"])
    except SlackApiError as e:
        print(slack_bot_token)
        print(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    send_message()
