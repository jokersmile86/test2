import json
import os
from datetime import datetime

DATA_FILE = "attendance.json"


def load_records():
    """저장된 출석 데이터를 불러온다."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_records(records):
    """출석 데이터를 저장한다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def input_date():
    """날짜를 YYYY-MM-DD 형식으로 입력받는다. 빈칸이면 오늘 날짜."""
    while True:
        date_text = input("날짜를 입력하세요 (YYYY-MM-DD, 엔터=오늘): ").strip()
        if date_text == "":
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. 예: 2026-11-02")


def input_name():
    """이름을 입력받는다."""
    while True:
        name = input("이름을 입력하세요: ").strip()
        if name:
            return name
        print("이름은 비워둘 수 없습니다.")


def add_record(records):
    """출석 기록 1개를 추가한다."""
    date_text = input_date()
    name = input_name()

    records.append({
        "date": date_text,
        "name": name
    })

    save_records(records)
    print(f"출석이 저장되었습니다. ({date_text}, {name})")


def list_records(records):
    """저장된 출석 목록을 보여준다."""
    if not records:
        print("저장된 출석 기록이 없습니다.")
        return

    # 날짜순 정렬, 같은 날짜면 이름순 정렬
    sorted_records = sorted(records, key=lambda x: (x["date"], x["name"]))

    print("\n=== 출석 목록 ===")
    for i, record in enumerate(sorted_records, start=1):
        print(f"{i}. {record['date']} - {record['name']}")
    print("=================\n")


def main():
    records = load_records()

    while True:
        print("출석부 프로그램")
        print("1. 출석 추가")
        print("2. 출석 목록 보기")
        print("3. 종료")

        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "1":
            add_record(records)
        elif choice == "2":
            list_records(records)
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 고르세요.")


if __name__ == "__main__":
    main()
