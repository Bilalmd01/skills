import sys
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
# The .env file should be in the skill's root directory (e.g., skills/korail-manager/.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

# Add local lib to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from korail2 import Korail

def main():
    # Load credentials from environment variables
    KORAIL_ID = os.environ.get("KORAIL_ID")
    KORAIL_PW = os.environ.get("KORAIL_PW")

    if not KORAIL_ID or not KORAIL_PW:
        print("❌ 오류: KORAIL_ID, KORAIL_PW 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)

    try:
        korail = Korail(KORAIL_ID, KORAIL_PW)
        reservations = korail.reservations()
        
        if not reservations:
            print("✅ 취소할 예약이 없습니다.")
            return

        for r in reservations:
            print(f"🔥 취소 시도: {r}")
            try:
                korail.cancel(r)
                print("✅ 취소 요청 완료")
            except Exception as e:
                # Patched korail2 might still raise error depending on version, but we ignore 'Extra data'
                if "Extra data" in str(e):
                    print("⚠️ 응답 해석 오류(무시)")
                else:
                    print(f"❌ 오류: {e}")

    except Exception as e:
        print(f"❌ 시스템 오류: {e}")

if __name__ == "__main__":
    main()
