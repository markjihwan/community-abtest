#!/bin/bash
# Hook: experiments/ 파일에 "ship" 결론 저장 시 guardrail 체크 확인
# Event: PreToolUse (Write|Edit)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // empty')

# experiments/ 디렉토리의 .md 파일만 체크
if echo "$FILE_PATH" | grep -q "experiments/.*\.md" && ! echo "$FILE_PATH" | grep -q "TEMPLATE"; then
  # "ship" 결론이 포함된 경우에만 검사
  if echo "$CONTENT" | grep -qi "결론.*ship\|decision.*ship\|판정.*ship"; then

    # Guardrail 체크 결과가 명시되어 있는지 확인
    if ! echo "$CONTENT" | grep -qi "guardrail.*안전\|guardrail.*pass\|guardrail.*✅\|guardrail.*ok"; then
      echo "[ship 차단] Guardrail 체크 결과가 명시되지 않았습니다." >&2
      echo "ship 결론 전에 Guardrail 지표 상태(안전/경계/훼손)를 먼저 기록해주세요." >&2
      exit 2
    fi

  fi
fi

exit 0
