"""
CSV로 foods 테이블 초기 데이터 삽입.

사용법:
  cd minahai
  python scripts/seed_foods.py <CSV_경로>

예:
  python scripts/seed_foods.py "c:/Users/hi/Downloads/농림수산식품교육문화정보원_칼로리 정보_20190926.csv"
"""

import asyncio
import csv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BACKEND_DIR / "apps"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(APPS_DIR))

load_dotenv(BACKEND_DIR / ".env")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

from inbody.adapter.outbound.orm.food_orm import Food


def _parse_float(value: str) -> float:
    try:
        return float(value.strip()) if value.strip() else 0.0
    except ValueError:
        return 0.0


async def seed(csv_path: str) -> None:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL이 .env에 없습니다.")

    if "+psycopg" not in database_url:
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        elif database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)

    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    rows: list[dict] = []
    with open(csv_path, encoding="euc-kr", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("음식명", "").strip()
            if not name:
                continue
            rows.append({
                "name": name,
                "calories_kcal": _parse_float(row.get("1인분칼로리(kcal)", "0")),
                "protein_g": _parse_float(row.get("단백질(g)", "0")),
                "carbs_g": _parse_float(row.get("탄수화물(g)", "0")),
                "fat_g": _parse_float(row.get("지방(g)", "0")),
                "serving_size": 1.0,
                "serving_unit": "인분",
                "created_by": None,
            })

    async with async_session() as session:
        existing = set(
            r[0] for r in (await session.execute(select(Food.name))).all()
        )
        new_rows = [r for r in rows if r["name"] not in existing]

        if not new_rows:
            print("추가할 새 데이터가 없습니다.")
            return

        session.add_all([Food(**r) for r in new_rows])
        await session.commit()
        print(f"완료: {len(new_rows)}개 삽입 (이미 존재 {len(rows) - len(new_rows)}개 건너뜀)")

    await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python scripts/seed_foods.py <CSV_경로>")
        sys.exit(1)
    asyncio.run(seed(sys.argv[1]))
