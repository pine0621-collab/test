"""증시 데이터 수집 모듈"""
import yfinance as yf
from datetime import datetime
import pytz


def get_market_summary() -> dict:
    """코스피, 코스닥, 주요 지수 데이터를 가져옵니다."""

    indices = {
        "코스피": "^KS11",
        "코스닥": "^KQ11",
        "다우존스": "^DJI",
        "나스닥": "^IXIC",
        "S&P 500": "^GSPC",
    }

    major_stocks = {
        "삼성전자": "005930.KS",
        "SK하이닉스": "000660.KS",
        "현대차": "005380.KS",
        "NAVER": "035420.KS",
        "카카오": "035720.KS",
    }

    result = {
        "indices": {},
        "stocks": {},
        "timestamp": datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M"),
    }

    # 주요 지수 데이터
    for name, ticker in indices.items():
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="2d")
            if len(hist) >= 1:
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change = current - prev
                change_pct = (change / prev) * 100 if prev != 0 else 0
                result["indices"][name] = {
                    "price": current,
                    "change": change,
                    "change_pct": change_pct,
                }
        except Exception as e:
            print(f"[경고] {name} 데이터 가져오기 실패: {e}")

    # 주요 종목 데이터
    for name, ticker in major_stocks.items():
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="2d")
            if len(hist) >= 1:
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change = current - prev
                change_pct = (change / prev) * 100 if prev != 0 else 0
                result["stocks"][name] = {
                    "price": current,
                    "change": change,
                    "change_pct": change_pct,
                }
        except Exception as e:
            print(f"[경고] {name} 데이터 가져오기 실패: {e}")

    return result


def format_market_message(data: dict) -> str:
    """증시 데이터를 Slack 메시지 형식으로 포맷합니다."""

    def format_change(change: float, change_pct: float) -> str:
        emoji = "📈" if change >= 0 else "📉"
        sign = "+" if change >= 0 else ""
        return f"{emoji} {sign}{change:,.2f} ({sign}{change_pct:.2f}%)"

    lines = [
        f"## 📊 오늘의 증시 현황 ({data['timestamp']})",
        "",
        "### 주요 지수",
    ]

    for name, info in data["indices"].items():
        price_str = f"{info['price']:,.2f}"
        change_str = format_change(info["change"], info["change_pct"])
        lines.append(f"• **{name}**: {price_str} {change_str}")

    lines.extend(["", "### 국내 주요 종목"])

    for name, info in data["stocks"].items():
        price_str = f"{info['price']:,.0f}원"
        change_str = format_change(info["change"], info["change_pct"])
        lines.append(f"• **{name}**: {price_str} {change_str}")

    lines.extend([
        "",
        "---",
        "_좋은 하루 되세요!_ ☀️",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    # 테스트 실행
    data = get_market_summary()
    print(format_market_message(data))
