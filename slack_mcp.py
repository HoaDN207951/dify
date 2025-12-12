from fastmcp import FastMCP
from pydantic import BaseModel
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime

app = FastMCP(
    name="mcp-slack-server",
    version="0.2.0",
)

# --------------------------
#  Tool Input Schemas
# --------------------------

class PostMessageInput(BaseModel):
    bot_token: str
    channel_id: str
    text: str


class ListChannelsInput(BaseModel):
    bot_token: str
    limit: int | None = 20


class GetHistoryInput(BaseModel):
    bot_token: str
    channel_id: str
    limit: int | None = 10


# --------------------------
#  Tools
# --------------------------

@app.tool()
def post_message(params: PostMessageInput) -> str:
    """
    Post a message to a Slack channel.
    """
    slack = WebClient(token=params.bot_token)

    try:
        result = slack.chat_postMessage(
            channel=params.channel_id,
            text=params.text
        )
        return f"Successfully posted to {params.channel_id}. Ts: {result['ts']}"

    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")


@app.tool()
def list_channels(params: ListChannelsInput) -> str:
    """
    List visible public channels.
    """
    slack = WebClient(token=params.bot_token)

    try:
        result = slack.conversations_list(
            limit=params.limit,
            types="public_channel"
        )

        channels = result.get("channels", [])
        if not channels:
            return "No channels found."

        formatted = [
            f"[{c['id']}] #{c['name']} ({c.get('num_members', 0)} members)"
            for c in channels
        ]
        return "\n".join(formatted)

    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")


@app.tool()
def get_history(params: GetHistoryInput) -> str:
    """
    Get channel message history.
    """
    slack = WebClient(token=params.bot_token)

    try:
        result = slack.conversations_history(
            channel=params.channel_id,
            limit=params.limit
        )

        messages = result.get("messages", [])
        if not messages:
            return "No messages found."

        formatted = []
        for m in messages:
            ts = float(m["ts"])
            ts_str = datetime.datetime.utcfromtimestamp(ts).isoformat()
            user = m.get("user") or m.get("bot_id") or "unknown"
            text = m.get("text", "")
            formatted.append(f"[{ts_str}] {user}: {text}")

        return "\n".join(formatted)

    except SlackApiError as e:
        raise RuntimeError(f"Slack API error: {e.response['error']}")


# --------------------------
#  Run MCP Server
# --------------------------

if __name__ == "__main__":
    app.run(transport="sse")
