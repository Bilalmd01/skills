#!/bin/bash
set -e

# 스크립트의 위치를 기준으로 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

echo "🔨 대장간(가상 환경) 건설을 시작하옵니다..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 대장간 건설 완료."
else
    echo "ℹ️ 대장간이 이미 존재하옵니다."
fi

echo "📦 필요한 부품(의존성)을 설치하옵니다..."
# 가상 환경의 pip 사용
./venv/bin/pip install -r requirements.txt

echo "🎉 모든 준비가 완료되었나이다! 이제 'korail-manager'를 즉시 사용하실 수 있사옵니다."
