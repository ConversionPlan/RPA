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


def load_and_convert_results():
    """Load JSON and convert BehaveX format to standard Behave format if needed"""
    # Try to load report.json (BehaveX format) first
    json_path = "./report/output/report.json"
    if not os.path.exists(json_path):
        json_path = "./report/output/results.json"

    with open(json_path, "r") as file:
        json_data = json.load(file)

    # Detect if it's BehaveX format (has 'features' key)
    if isinstance(json_data, dict) and "features" in json_data:
        # Convert BehaveX format to standard Behave format
        converted = []
        for feature in json_data["features"]:
            converted_feature = {
                "keyword": "Feature",
                "name": feature["name"],
                "tags": [{"name": tag, "line": 1} for tag in feature.get("scenarios", [{}])[0].get("tags", [])],
                "elements": []
            }
            for scenario in feature.get("scenarios", []):
                converted_feature["elements"].append({
                    "name": scenario["name"],
                    "status": scenario["status"],
                    "steps": scenario.get("steps", [])
                })
            converted.append(converted_feature)
        return converted

    return json_data

def format_results():
    any_errors = False
    status_names = {
        "passed": ":white_check_mark: Passed",
        "failed": ":x: Failed",
        "skipped": ":ballot_box_with_check: Skipped",
        "error": ":x: Error",
        "undefined": ":question: Undefined",
        "untested": ":ballot_box_with_check: Skipped",
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

    json_data = load_and_convert_results()

    for feature in json_data:
        if feature.get("tags") and len(feature["tags"]) > 0:
            first_tag = feature["tags"][0]
            if isinstance(first_tag, dict):
                first_tag = first_tag.get("name", "")
            if first_tag == "Ignore":
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

        try:
            feature["elements"]
        except KeyError:
            continue

        for scenario in feature["elements"]:
            status = status_names.get(scenario["status"], ":question: Unknown")
            formatted_results.append(
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{scenario["name"]}: {status}"},
                }
            )

            if scenario["status"] in ["failed", "error"]:
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
                                        "text": f"Error:\n```{error_message[:200]}```",
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
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":alert: @here There was an error with the tests, but it couldn't be sent, check the https://github.com/ConversionPlan/RPA/actions/. :alert:",
                    },
                }
            ],
        )
        print(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    send_message()
