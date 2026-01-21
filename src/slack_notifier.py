"""Slack 알림 모듈"""
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackNotifier:
    """Slack 채널로 메시지를 전송하는 클래스"""

    def __init__(self, token: str = None, channel: str = None):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.channel = channel or os.getenv("SLACK_CHANNEL_ID")
        self.client = WebClient(token=self.token)

    def send_message(self, message: str) -> bool:
        """Slack 채널에 메시지를 전송합니다."""
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=message,
                mrkdwn=True,
            )
            print(f"[성공] 메시지 전송 완료 (ts: {response['ts']})")
            return True
        except SlackApiError as e:
            print(f"[오류] Slack 메시지 전송 실패: {e.response['error']}")
            return False

    def send_blocks(self, blocks: list, text: str = "증시 알림") -> bool:
        """Slack Block Kit 형식으로 메시지를 전송합니다."""
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=text,
                blocks=blocks,
            )
            print(f"[성공] 블록 메시지 전송 완료 (ts: {response['ts']})")
            return True
        except SlackApiError as e:
            print(f"[오류] Slack 블록 메시지 전송 실패: {e.response['error']}")
            return False


def create_market_blocks(data: dict) -> list:
    """증시 데이터를 Slack Block Kit 형식으로 변환합니다."""

    def format_change(change: float, change_pct: float) -> str:
        emoji = ":chart_with_upwards_trend:" if change >= 0 else ":chart_with_downwards_trend:"
        sign = "+" if change >= 0 else ""
        return f"{emoji} {sign}{change:,.2f} ({sign}{change_pct:.2f}%)"

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📊 오늘의 증시 현황 ({data['timestamp']})",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*주요 지수*",
            },
        },
    ]

    # 지수 정보
    indices_text = []
    for name, info in data["indices"].items():
        price_str = f"{info['price']:,.2f}"
        change_str = format_change(info["change"], info["change_pct"])
        indices_text.append(f"• *{name}*: {price_str} {change_str}")

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "\n".join(indices_text),
        },
    })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*국내 주요 종목*",
        },
    })

    # 종목 정보
    stocks_text = []
    for name, info in data["stocks"].items():
        price_str = f"{info['price']:,.0f}원"
        change_str = format_change(info["change"], info["change_pct"])
        stocks_text.append(f"• *{name}*: {price_str} {change_str}")

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "\n".join(stocks_text),
        },
    })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "_좋은 하루 되세요!_ :sunny:",
            },
        ],
    })

    return blocks


if __name__ == "__main__":
    # 테스트
    from dotenv import load_dotenv
    load_dotenv()

    notifier = SlackNotifier()
    notifier.send_message("테스트 메시지입니다.")
