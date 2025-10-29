import os
import json
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import time

load_dotenv()

# Try to get token from environment variable first, then from .env file
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
if not slack_bot_token:
    print("[WARNING] SLACK_BOT_TOKEN not found in environment variables, checking .env file...")
    from dotenv import dotenv_values
    config = dotenv_values(".env")
    slack_bot_token = config.get("SLACK_BOT_TOKEN")
    if not slack_bot_token:
        print("[ERROR] SLACK_BOT_TOKEN not found in .env file either!")

channel_id = "C084F8LFU94"

# GitHub context from environment variables
github_context = {
    "repository": os.environ.get("GITHUB_REPOSITORY", "Unknown"),
    "run_id": os.environ.get("GITHUB_RUN_ID", ""),
    "run_number": os.environ.get("GITHUB_RUN_NUMBER", ""),
    "actor": os.environ.get("GITHUB_ACTOR", "Unknown"),
    "sha": os.environ.get("GITHUB_SHA", "")[:7] if os.environ.get("GITHUB_SHA") else "",
    "ref": os.environ.get("GITHUB_REF", "").replace("refs/heads/", ""),
    "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
    "server_url": os.environ.get("GITHUB_SERVER_URL", "https://github.com"),
    "event_name": os.environ.get("GITHUB_EVENT_NAME", ""),
}

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


def calculate_statistics(json_data):
    """Calculate detailed statistics from test results"""
    stats = {
        "total_features": 0,
        "total_scenarios": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "error": 0,
        "undefined": 0,
        "success_rate": 0.0,
        "feature_details": [],
        "execution_time": 0,
    }

    start_time = None
    end_time = None

    for feature in json_data:
        if feature.get("tags") and len(feature["tags"]) > 0:
            first_tag = feature["tags"][0]
            if isinstance(first_tag, dict):
                first_tag = first_tag.get("name", "")
            if first_tag == "Ignore":
                continue

        stats["total_features"] += 1
        feature_stats = {
            "name": feature["name"],
            "passed": 0,
            "failed": 0,
            "total": 0,
        }

        if "elements" not in feature:
            continue

        for scenario in feature["elements"]:
            stats["total_scenarios"] += 1
            feature_stats["total"] += 1
            status = scenario.get("status", "undefined")

            if status == "passed":
                stats["passed"] += 1
                feature_stats["passed"] += 1
            elif status == "failed":
                stats["failed"] += 1
                feature_stats["failed"] += 1
            elif status == "skipped" or status == "untested":
                stats["skipped"] += 1
            elif status == "error":
                stats["error"] += 1
                feature_stats["failed"] += 1
            else:
                stats["undefined"] += 1

        feature_stats["success_rate"] = (
            (feature_stats["passed"] / feature_stats["total"] * 100)
            if feature_stats["total"] > 0
            else 0
        )
        stats["feature_details"].append(feature_stats)

    if stats["total_scenarios"] > 0:
        stats["success_rate"] = (stats["passed"] / stats["total_scenarios"]) * 100

    return stats


def format_results():
    """Format test results with comprehensive information for Slack"""
    any_errors = False
    status_names = {
        "passed": ":white_check_mark: Passed",
        "failed": ":x: Failed",
        "skipped": ":ballot_box_with_check: Skipped",
        "error": ":x: Error",
        "undefined": ":question: Undefined",
        "untested": ":ballot_box_with_check: Skipped",
    }

    today = datetime.now().strftime("%B %d, %Y at %H:%M UTC")
    json_data = load_and_convert_results()
    stats = calculate_statistics(json_data)

    # Determine overall status emoji
    if stats["failed"] == 0 and stats["error"] == 0:
        status_emoji = ":white_check_mark:"
        status_text = "ALL TESTS PASSED"
        status_color = "#36a64f"
    elif stats["success_rate"] >= 80:
        status_emoji = ":warning:"
        status_text = "TESTS PASSED WITH WARNINGS"
        status_color = "#ff9900"
    else:
        status_emoji = ":x:"
        status_text = "TESTS FAILED"
        status_color = "#ff0000"
        any_errors = True

    # Build GitHub links
    actions_url = ""
    commit_url = ""
    if github_context["run_id"]:
        actions_url = f"{github_context['server_url']}/{github_context['repository']}/actions/runs/{github_context['run_id']}"
    if github_context["sha"]:
        commit_url = f"{github_context['server_url']}/{github_context['repository']}/commit/{github_context['sha']}"

    # Header section
    formatted_results = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{status_emoji} RPA Test Report - {status_text}",
            },
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Date:*\n{today}"},
                {"type": "mrkdwn", "text": f"*Workflow:*\n{github_context['workflow'] or 'RPA Tests'}"},
                {"type": "mrkdwn", "text": f"*Branch:*\n`{github_context['ref'] or 'main'}`"},
                {"type": "mrkdwn", "text": f"*Triggered by:*\n{github_context['actor']}"},
                {"type": "mrkdwn", "text": f"*Event:*\n{github_context['event_name'] or 'push'}"},
                {"type": "mrkdwn", "text": f"*Run:*\n#{github_context['run_number'] or 'N/A'}"},
            ],
        },
    ]

    # Add commit info if available
    if commit_url:
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Commit:* <{commit_url}|`{github_context['sha']}`>",
            },
        })

    formatted_results.append({"type": "divider"})

    # Statistics section
    formatted_results.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*:bar_chart: Overall Statistics*",
        },
    })

    formatted_results.append({
        "type": "section",
        "fields": [
            {"type": "mrkdwn", "text": f"*Total Features:*\n{stats['total_features']}"},
            {"type": "mrkdwn", "text": f"*Total Scenarios:*\n{stats['total_scenarios']}"},
            {"type": "mrkdwn", "text": f"*:white_check_mark: Passed:*\n{stats['passed']}"},
            {"type": "mrkdwn", "text": f"*:x: Failed:*\n{stats['failed']}"},
            {"type": "mrkdwn", "text": f"*:ballot_box_with_check: Skipped:*\n{stats['skipped']}"},
            {"type": "mrkdwn", "text": f"*Success Rate:*\n{stats['success_rate']:.1f}%"},
        ],
    })

    # Progress bar
    if stats["total_scenarios"] > 0:
        passed_blocks = int((stats["passed"] / stats["total_scenarios"]) * 10)
        failed_blocks = int((stats["failed"] / stats["total_scenarios"]) * 10)
        progress_bar = "█" * passed_blocks + "▓" * failed_blocks + "░" * (10 - passed_blocks - failed_blocks)
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"```{progress_bar}``` {stats['success_rate']:.1f}% success",
            },
        })

    formatted_results.append({"type": "divider"})

    # Feature-by-feature breakdown (compact format)
    formatted_results.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*:file_folder: Feature Results*",
        },
    })

    # Combine feature details into fewer blocks (max 10 lines per block)
    feature_lines = []
    for feature_stat in stats["feature_details"]:
        feature_emoji = ":white_check_mark:" if feature_stat["failed"] == 0 else ":x:"
        feature_lines.append(f"{feature_emoji} *{feature_stat['name']}* - {feature_stat['passed']}/{feature_stat['total']} ({feature_stat['success_rate']:.0f}%)")

    # Split into blocks of 10 features each
    for i in range(0, len(feature_lines), 10):
        chunk = feature_lines[i:i+10]
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n".join(chunk),
            },
        })

    formatted_results.append({"type": "divider"})

    # Detailed scenario results (for failures) - Compact format
    has_failures = False
    failure_details = []

    for feature in json_data:
        if feature.get("tags") and len(feature["tags"]) > 0:
            first_tag = feature["tags"][0]
            if isinstance(first_tag, dict):
                first_tag = first_tag.get("name", "")
            if first_tag == "Ignore":
                continue

        if "elements" not in feature:
            continue

        for scenario in feature["elements"]:
            if scenario["status"] in ["failed", "error"]:
                any_errors = True
                has_failures = True

                # Collect failure info
                error_info = f":x: *{feature['name']}* → {scenario['name']}"

                # Find first failed step
                for step in scenario.get("steps", []):
                    try:
                        if step["result"]["status"] == "failed":
                            error_message = "\n".join(step["result"]["error_message"])
                            error_info += f"\n`{step['name']}`\n```{error_message[:200]}```"
                            break  # Only show first failed step
                    except (KeyError, TypeError):
                        pass

                failure_details.append(error_info)

    # Add failures section if any
    if has_failures:
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*:mag: Failed Scenarios Details*",
            },
        })

        # Combine all failures into one or two blocks
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\n\n".join(failure_details[:5]),  # Max 5 failures shown
            },
        })

        if len(failure_details) > 5:
            formatted_results.append({
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"_...and {len(failure_details) - 5} more failures. Check artifacts for full details._"}
                ],
            })

    formatted_results.append({"type": "divider"})

    # Links section
    formatted_results.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*:link: Quick Links*",
        },
    })

    links_text = ""
    if actions_url:
        links_text += f"• <{actions_url}|:arrow_forward: View GitHub Actions Run>\n"
        links_text += f"• <{actions_url}#artifacts|:package: Download Artifacts>\n"
    if commit_url:
        links_text += f"• <{commit_url}|:git: View Commit>\n"

    # Add MinIO link if available
    minio_endpoint = os.environ.get("MINIO_ENDPOINT", "")
    minio_bucket = os.environ.get("MINIO_BUCKET", "")
    if minio_endpoint and minio_bucket:
        links_text += f"• <{minio_endpoint}/{minio_bucket}|:file_cabinet: View Reports in S3>\n"

    if links_text:
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": links_text,
            },
        })

    formatted_results.append({"type": "divider"})

    # Conclusion section
    formatted_results.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":robot_face: Summary",
        },
    })

    if any_errors:
        mention = "@here" if stats["success_rate"] < 50 else "@channel"
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":alert: {mention} *{stats['failed']} scenario(s) failed!* Please investigate as soon as possible.\n\nReact with :eyes: once you are looking into it.",
            },
        })
    else:
        formatted_results.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":tada: *All {stats['total_scenarios']} scenarios passed successfully!* Great work team! :tada:",
            },
        })

    # Add action buttons
    if actions_url:
        formatted_results.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":arrow_forward: View Run"},
                    "url": actions_url,
                    "style": "primary" if not any_errors else "danger",
                },
            ],
        })

    # Slack has a limit of 50 blocks per message
    if len(formatted_results) > 50:
        print(f"[WARNING] Message has {len(formatted_results)} blocks, exceeding Slack's 50 block limit!")
        print(f"[WARNING] Trimming message to fit within limit...")
        # Keep header, stats, and conclusion, trim the middle
        formatted_results = formatted_results[:25] + [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "_Message truncated due to Slack's 50 block limit. Check GitHub Actions for full details._",
                },
            },
            {"type": "divider"},
        ] + formatted_results[-20:]

    print(f"[INFO] Final message has {len(formatted_results)} blocks")
    return formatted_results, any_errors


def send_message():
    """Send formatted test results to Slack with enhanced notifications"""
    try:
        print(f"[INFO] Starting Slack notification process...")
        print(f"[DEBUG] Channel ID: {channel_id}")
        print(f"[DEBUG] Token present: {'Yes' if slack_bot_token else 'No'}")
        print(f"[DEBUG] GitHub Context: Repository={github_context['repository']}, Run={github_context['run_number']}")

        message, has_errors = format_results()
        print(f"[DEBUG] Message formatted successfully with {len(message)} blocks")
        print(f"[DEBUG] Test status: {'FAILED' if has_errors else 'PASSED'}")

        # Send main message
        response = client.chat_postMessage(
            channel=channel_id,
            blocks=message,
            text=f"RPA Test Report - {'FAILED' if has_errors else 'PASSED'}",  # Fallback text for notifications
        )

        print(f"[SUCCESS] Message sent successfully! Timestamp: {response['ts']}")
        print(f"[SUCCESS] Channel: {channel_id}")

        # Add thread with additional context if needed
        if has_errors and github_context["run_id"]:
            actions_url = f"{github_context['server_url']}/{github_context['repository']}/actions/runs/{github_context['run_id']}"
            try:
                client.chat_postMessage(
                    channel=channel_id,
                    thread_ts=response['ts'],
                    text=f":point_right: Quick actions:\n• View full logs: {actions_url}\n• Download artifacts: {actions_url}#artifacts\n• Check workflow file: {github_context['server_url']}/{github_context['repository']}/blob/main/.github/workflows/github-actions.yml",
                )
                print(f"[SUCCESS] Thread with quick actions added")
            except Exception as thread_error:
                print(f"[WARNING] Could not add thread: {thread_error}")

        return True

    except SlackApiError as e:
        print(f"[ERROR] SlackApiError occurred: {e.response['error']}")
        print(f"[ERROR] Full error details: {e}")

        # Try to send a fallback message
        try:
            actions_url = f"{github_context['server_url']}/{github_context['repository']}/actions"
            response = client.chat_postMessage(
                channel=channel_id,
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":warning: RPA Test Report - Error",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":alert: @here There was an error generating the test report.\n\nPlease check <{actions_url}|GitHub Actions> manually.",
                        },
                    },
                ],
            )
            print(f"[INFO] Fallback message sent successfully")
            return False
        except Exception as fallback_error:
            print(f"[ERROR] Could not send fallback message: {fallback_error}")
            return False

    except Exception as e:
        print(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    send_message()
