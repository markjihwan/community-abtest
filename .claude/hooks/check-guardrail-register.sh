#!/bin/bash
# Hook: experiments/ 파일 저장 시 Guardrail 누락 확인
# Event: PreToolUse (Write|Edit)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // empty')

# experiments/ 디렉토리의 .md 파일만 체크 (TEMPLATE.md 제외)
if echo "$FILE_PATH" | grep -q "experiments/.*\.md" && ! echo "$FILE_PATH" | grep -q "TEMPLATE"; then
  # Guardrail 섹션이 없으면 차단
  if ! echo "$CONTENT" | grep -qi "guardrail"; then
    echo "Guardrail 지표가 정의되지 않았습니다. 실험 등록서에 Guardrail을 추가한 뒤 저장하세요." >&2
    exit 2
  fi

  # Guardrail 값이 비어있으면 (<!-- ... --> 또는 빈 줄만) 경고
  if echo "$CONTENT" | grep -i "guardrail" | grep -q "<!--"; then
    echo "Guardrail 지표가 주석 처리되어 있습니다. 실제 값을 입력해주세요." >&2
    exit 2
  fi
fi

exit 0
