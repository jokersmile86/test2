# 🐳 Docker 웹서버 프로젝트

## 📌 프로젝트 소개
nginx 기반 Docker 컨테이너로 간단한 웹페이지를 띄우는 프로젝트입니다.

## 🛠️ 사용 기술
- Docker (nginx)
- HTML
- Git / GitHub

## 📂 4. 폴더 구조
```text
.
├── app/
│   └── index.html
├── Dockerfile
├── attend.py
└── README.md
```

---

## 🚀 수행 내용 및 실행 방법

### ① Git 설정 확인
```bash
git config --list
```

### ② 터미널 조작 및 권한 실습
```bash
mkdir -p app
echo "Docker 웹서버 미션 v1" > app/index.html
ls -l app/index.html
chmod 755 app/index.html
ls -l app/index.html
```

### ③ Docker 설치 점검 및 커스텀 이미지 빌드
1. **버전 및 데몬 점검**
   ```bash
   docker --version
   docker info
   ```
2. **이미지 빌드**
   ```bash
   docker build -t my-web:1.0 .
   ```

### ④ 컨테이너 실행 (바인드 마운트) 및 접속
1. **컨테이너 실행**
   ```bash
   docker run -d --name web -p 8080:80 -v ${PWD}/app:/usr/share/nginx/html my-web:1.0
   ```
2. **브라우저 접속**
   - 주소창 입력: `http://localhost:8080`
   - 터미널 확인: `curl http://localhost:8080`

### ⑤ Docker 볼륨 영속성 검증
```bash
docker volume create my_work_vol
docker run -d --name vol-test -v my_work_vol:/data ubuntu sleep infinity
docker exec -it vol-test bash -c "echo 'Persisted Data' > /data/memo.txt"
docker rm -f vol-test
# 컨테이너 삭제 후 데이터 유지 확인
docker run --rm -v my_work_vol:/data ubuntu cat /data/memo.txt
```

---

## 🚨 트러블슈팅 (Troubleshooting)

### 트러블슈팅 1: 파일 수정 후 브라우저 새로고침 시 내용이 즉시 반영되지 않던 문제
- **문제 상황:** 빌드 후 `app/index.html`을 수정했으나 브라우저 화면이 이전 상태에서 바뀌지 않음.
- **원인 가설:** 일반 `COPY` 명령어로 생성된 이미지는 파일이 이미지 내부 레이어에 **정적 복사**되므로, 호스트의 원본 소스가 바뀌어도 컨테이너 내부 파일은 갱신되지 않기 때문.
- **해결/대안:** 컨테이너 실행 시 `-v` 옵션(바인드 마운트)을 사용하여 호스트의 디렉토리와 컨테이너 내부 경로를 직접 연결(`-v ${PWD}/app:/usr/share/nginx/html`)하여 실시간 동기화 환경을 구축함.

### 트러블슈팅 2: Git 푸시 전후 설정 및 상태 관리
- **문제 상황:** 작업 폴더 변경 사항을 원격 저장소에 올릴 때 브랜치 및 사용자 정보 매칭 필요.
- **원인 가설:** 로컬 커밋 내역이 원격 저장소(`origin/main`)와 올바르게 동기화되지 않으면 충돌이 발생할 수 있음.
- **해결/대안:** `git add .`, `git commit -m "..."`, `git push` 순서로 안전하게 형상 관리를 완료함.

---

## 💡 7. 배운 점
- COPY(복사본)와 바인드 마운트(실시간 연결)의 차이를 직접 실험으로 이해함.
- Docker를 활용해 환경에 구애받지 않는 재현 가능한 웹 서버 실행 환경을 구축하는 방법을 체득함.