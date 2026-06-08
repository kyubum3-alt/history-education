#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
역사교육학 홈페이지 자동 배포 스크립트
posts.json 수정 + Git 커밋/푸시 자동화
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 설정
REPO_DIR = Path(__file__).parent
POSTS_JSON = REPO_DIR / "posts.json"

def run_git_command(cmd, cwd=None):
    """Git 명령어 실행"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or REPO_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0:
            print(f"❌ 오류: {result.stderr}")
            return False
        print(f"✅ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ 명령어 실행 실패: {e}")
        return False

def add_spanish_papers(papers_data):
    """posts.json에 스페인어권 논문 추가"""
    try:
        with open(POSTS_JSON, 'r', encoding='utf-8') as f:
            posts = json.load(f)

        # 기존 spanish 배열에 앞에 추가
        for paper in reversed(papers_data):
            posts['spanish'].insert(0, paper)

        # 파일 저장 (CRLF 유지)
        with open(POSTS_JSON, 'w', encoding='utf-8', newline='') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

        print(f"✅ posts.json 업데이트 완료: {len(papers_data)}개 논문 추가")
        return True
    except Exception as e:
        print(f"❌ JSON 수정 실패: {e}")
        return False

def commit_and_push(message):
    """변경사항 커밋 및 푸시"""
    print("\n📤 Git 작업 시작...\n")

    # Git add
    if not run_git_command("git add posts.json"):
        return False

    # Git commit
    if not run_git_command(f'git commit -m "{message}"'):
        return False

    # Git push
    if not run_git_command("git push origin main"):
        return False

    print("\n✅ GitHub 푸시 완료!")
    return True

def main():
    """메인 함수"""
    print("🚀 역사교육학 홈페이지 배포 스크립트 시작\n")

    # 추가할 스페인어권 논문 데이터
    new_papers = [
        {
            "title": "교육개혁과 역사교육",
            "authors": "Delgado",
            "year": 2023,
            "url": "Delgado_2023_교육개혁과_역사교육_한국어번역.html",
            "uploadDate": "2026-05-13"
        },
        {
            "title": "학교의 역사적 기억",
            "authors": "Diez",
            "year": 2022,
            "url": "Diez_2022_학교의_역사적_기억_한국어번역.html",
            "uploadDate": "2026-05-13"
        },
        {
            "title": "스페인 역사 (LOMLOE)",
            "authors": "스페인 교육과정",
            "year": 2022,
            "url": "Historia_de_Espana_LOMLOE.html",
            "uploadDate": "2026-05-13"
        }
    ]

    # 1. posts.json 수정
    print("📝 posts.json 수정 중...")
    if not add_spanish_papers(new_papers):
        sys.exit(1)

    # 2. Git 커밋 및 푸시
    message = "Update posts.json with 3 new Spanish education papers (Delgado 2023, Diez 2022, LOMLOE 2022)"
    if not commit_and_push(message):
        sys.exit(1)

    print("\n🎉 배포 완료!")
    print("💡 팁: Ctrl+Shift+R로 캐시 무시 새로고침 후 확인하세요")

if __name__ == "__main__":
    main()
