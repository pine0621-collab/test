require("dotenv").config();
const cron = require("node-cron");
const { WebClient } = require("@slack/web-api");

const slack = new WebClient(process.env.SLACK_BOT_TOKEN);
const channel = process.env.SLACK_CHANNEL_ID;

const REMINDER_MESSAGE = [
  ":dart: *오늘의 몰입 업무 체크인*",
  "",
  "오늘 몰입한 업무와 몰입에 방해되는 업무는 무엇이셨나요?",
  "",
  "아래 양식으로 답변해 주세요:",
  "• :fire: *몰입한 업무:* ",
  "• :no_entry_sign: *몰입을 방해한 업무:* ",
  "",
  "매일 기록하면 나의 업무 패턴이 보입니다 :eyes:",
].join("\n");

async function sendReminder() {
  try {
    await slack.chat.postMessage({
      channel,
      text: REMINDER_MESSAGE,
      unfurl_links: false,
    });
    console.log(
      `[${new Date().toISOString()}] 몰입 업무 리마인더 전송 완료 → ${channel}`
    );
  } catch (error) {
    console.error(
      `[${new Date().toISOString()}] 리마인더 전송 실패:`,
      error.message
    );
  }
}

// 매일 오후 5시 (KST) 실행 — cron은 서버 로컬 시간 기준
// TZ 환경변수가 Asia/Seoul이면 17:00 KST
const cronExpression = process.env.CRON_SCHEDULE || "0 17 * * 1-5";

cron.schedule(cronExpression, () => {
  console.log(`[${new Date().toISOString()}] 스케줄 트리거됨`);
  sendReminder();
});

console.log("=".repeat(50));
console.log("Slack 몰입 업무 리마인더 봇 시작");
console.log(`채널: ${channel}`);
console.log(`스케줄: ${cronExpression}`);
console.log(`타임존: ${process.env.TZ || "system default"}`);
console.log("=".repeat(50));
