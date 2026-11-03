# 🐳 개발 워크스테이션 구축 및 Docker 웹 서버 미션

> **문서 목적:** Linux CLI, 파일 권한, Docker 이미지·컨테이너, 네트워크, 마운트 및 Docker Compose의 동작을 실습하고 검증한 내용을 정리합니다.
>
> **기록 원칙:** 아래 명령어는 실습 절차와 확인 방법을 정리한 것입니다. 실제 실행 결과를 기록할 때는 본인 환경에서 실행한 출력만 추가하고, 실행하지 않은 결과나 임의의 시간·컨테이너 ID를 작성하지 않습니다.

---

## 📌 1. 프로젝트 개요

### 미션 목표

- Linux CLI 환경과 기본 파일 조작 명령어 이해
- 파일 및 디렉터리 권한(`755`, `644`) 변경 원리 이해
- Docker 이미지와 컨테이너의 차이 및 컨테이너 격리 이해
- Dockerfile을 이용한 NGINX 기반 웹 서버 이미지 빌드
- 포트 매핑을 통한 호스트-컨테이너 통신 확인
- 바인드 마운트와 Docker 볼륨의 차이 및 데이터 영속성 검증
- Docker Compose를 이용한 멀티 컨테이너 구성과 서비스 간 통신 확인
- `.env`를 통한 설정값 분리
- GitHub SSH 인증 및 민감 정보 관리

### 주요 실습 내용

1. 터미널 위치 확인, 디렉터리 생성, 파일 생성·복사·이동·삭제
2. Linux 환경에서 `chmod`를 이용한 파일 권한 변경
3. Docker 설치 및 데몬 상태 확인
4. NGINX 기반 커스텀 이미지 빌드
5. 포트 매핑 후 브라우저 및 `curl` 접속
6. 바인드 마운트를 이용한 호스트 파일 변경 반영
7. Docker 볼륨을 이용한 컨테이너 삭제 후 데이터 유지 확인
8. Docker Compose로 `web`과 `cache` 서비스 실행
9. 서비스 이름을 이용한 컨테이너 간 통신 확인
10. 환경 변수 및 Git 보안 설정 적용

---

## 💻 2. 실행 환경

| 항목 | 환경 |
|---|---|
| OS | Windows 11 |
| 터미널 | VS Code Terminal / PowerShell |
| Linux 실습 환경 | WSL2 Ubuntu |
| Docker | Docker Desktop 27.2.0 |
| Docker Compose | Compose v2 |
| Git | Git 2.45.2.windows.1 |
| 웹 서버 | NGINX Alpine |
| 캐시 서비스 | Redis Alpine |

> **환경 구분:** Windows PowerShell과 WSL2 Ubuntu는 서로 다른 실행 환경입니다. Linux 권한 실습은 WSL2의 Linux 파일 시스템 안에서 진행합니다. 예를 들어 `/home/<사용자>/workspace` 경로를 사용하면 Linux 권한을 확인하기 쉽습니다. `/mnt/c` 아래의 Windows 파일 시스템은 마운트 옵션 등에 따라 Linux 권한 표시·동작이 달라질 수 있습니다.

---

## ✅ 3. 수행 항목 체크리스트

- [x] 터미널 위치 확인 및 디렉터리 구성
- [x] 파일 생성·복사·이동·삭제 명령어 실습
- [x] Linux 환경에서 파일 권한 변경 원리 확인
- [x] Docker 설치 및 데몬 상태 점검
- [x] 기본 컨테이너 실행
- [x] Dockerfile 작성 및 커스텀 이미지 빌드
- [x] 포트 매핑 및 웹 서버 접속 확인
- [x] 바인드 마운트의 파일 변경 반영 확인
- [x] Docker 볼륨의 데이터 영속성 검증
- [x] Docker Compose 단일·멀티 서비스 구성
- [x] Compose 네트워크에서 서비스 이름 기반 통신 확인
- [x] `.env`를 통한 호스트 포트 설정 분리
- [x] GitHub SSH 인증 설정
- [x] `.gitignore` 및 `.dockerignore` 적용

> 체크 항목은 실습 완료 여부에 맞게 유지합니다. 아직 재실행하거나 검증하지 않은 항목은 완료 표시를 해제하고, 실제 확인 후 체크합니다.

---

## 📂 4. 디렉터리 구조 및 설계 기준

```text
.
├── app/
│   └── index.html
├── images/
│   ├── browser.png
│   ├── build.png
│   └── compose_ps.png
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── .dockerignore
├── attend.py
├── attendance.json
└── README.md
```

| 파일·디렉터리 | 역할 |
|---|---|
| `app/` | NGINX가 제공할 정적 웹 콘텐츠 |
| `app/index.html` | 메인 웹 페이지 |
| `images/` | README에 연결한 실행 화면 이미지 |
| `Dockerfile` | 커스텀 웹 서버 이미지 빌드 명세 |
| `docker-compose.yml` | 여러 서비스와 네트워크 설정 |
| `.env` | Compose에서 사용할 환경 변수 |
| `.gitignore` | Git 추적에서 제외할 파일 지정 |
| `.dockerignore` | 이미지 빌드 컨텍스트에서 제외할 파일 지정 |
| `README.md` | 프로젝트 설명과 실습 절차 및 결과 기록 |

### 설계 기준

소스 코드(`app/`), 이미지 빌드 설정(`Dockerfile`), 서비스 구성(`docker-compose.yml`), 환경 설정(`.env`)을 분리했습니다. 이를 통해 소스 변경과 실행 환경 설정을 구분하고, Compose 명령어로 동일한 서비스 구성을 다시 실행할 수 있도록 구성했습니다.

### 보안 및 빌드 제외 설정

`.gitignore` 예시:

```gitignore
.env
*.key
id_ed25519
id_ed25519.pub
```

`.dockerignore` 예시:

```dockerignore
.git
.env
*.key
id_ed25519
id_ed25519.pub
README.md
images/
```

> `.env`에 비밀값이 포함되어 있다면 Git과 Docker 빌드 컨텍스트에서 제외합니다. 단, `.env`에 일반 포트 번호만 있더라도 프로젝트 정책에 따라 저장소 공개 여부를 결정합니다. 실제 개인키 파일은 절대로 저장소에 추가하지 않습니다. 공개키(`.pub`)는 개인키와 다르지만, 불필요한 파일 노출을 줄이기 위해 함께 제외할 수 있습니다.

---

## 📚 5. 핵심 개발 개념 정리

### 1) 절대 경로와 상대 경로

- **절대 경로:** 루트(`/`) 또는 드라이브(`C:\`)부터 시작하는 경로입니다.
- **상대 경로:** 현재 작업 디렉터리를 기준으로 한 경로입니다.

예시:

```bash
# Linux 절대 경로
/home/user/workspace/app

# 현재 디렉터리를 기준으로 한 상대 경로
./app/index.html
```

Docker 명령어에서 호스트 경로를 지정할 때는 현재 터미널이 PowerShell인지 WSL인지에 따라 경로 표현이 달라질 수 있습니다. Compose 파일 내부의 `./app`은 일반적으로 Compose 파일이 있는 디렉터리를 기준으로 해석됩니다.

### 2) 파일 권한과 숫자 표기법

Linux 권한은 소유자(Owner), 그룹(Group), 기타 사용자(Other) 순서로 표시합니다.

| 기호 | 의미 | 숫자 |
|---|---|---:|
| `r` | 읽기 | 4 |
| `w` | 쓰기 | 2 |
| `x` | 실행 | 1 |

- `755` = `rwxr-xr-x`: 소유자는 읽기·쓰기·실행, 그룹과 기타 사용자는 읽기·실행
- `644` = `rw-r--r--`: 소유자는 읽기·쓰기, 그룹과 기타 사용자는 읽기 전용

일반 HTML 파일은 보통 `644`, 디렉터리나 실행해야 하는 스크립트는 용도에 따라 `755`를 사용할 수 있습니다. 모든 파일에 무조건 `755`를 적용하는 것은 바람직하지 않습니다.

**중요:** Windows PowerShell의 `ls`는 Linux의 `ls -l`과 동일한 권한 표시를 제공하지 않습니다. PowerShell에서 `chmod`를 실행했다고 해서 NTFS 파일 권한이 Linux의 `rwx` 형태로 바뀌었다고 판단하면 안 됩니다. Linux 권한 변경 실습과 확인은 WSL2 Ubuntu의 Linux 파일 시스템에서 진행합니다.

### 3) 포트 매핑과 네트워크 네임스페이스

컨테이너는 자체 네트워크 환경에서 실행됩니다. `-p 9090:80`은 호스트의 9090번 포트로 들어온 요청을 컨테이너의 80번 포트로 전달하는 설정입니다.

```text
브라우저
   |
   | http://localhost:9090
   v
호스트 9090 포트
   |
   | Docker 포트 매핑
   v
컨테이너 80 포트
   |
   v
NGINX
```

포트 충돌이 발생하면 다음 명령어로 점유 상태를 확인할 수 있습니다.

PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 9090 -ErrorAction SilentlyContinue
```

Linux/WSL2:

```bash
ss -tulpn | grep ':9090'
```

기존 컨테이너가 포트를 사용 중이라면 `docker ps`로 확인한 뒤 해당 컨테이너를 중지하거나 Compose 프로젝트를 종료합니다.

### 4) 이미지, 컨테이너, 스토리지 방식

- **이미지(Image):** 컨테이너를 생성할 때 사용하는 읽기 전용 템플릿입니다.
- **컨테이너(Container):** 이미지로부터 생성되어 격리된 프로세스로 실행되는 인스턴스입니다. 컨테이너의 쓰기 계층에 기록한 데이터는 컨테이너 삭제 시 함께 사라질 수 있습니다.
- **COPY:** 빌드 시점에 파일을 이미지에 복사합니다.
- **바인드 마운트:** 호스트의 특정 경로를 컨테이너 경로에 연결합니다.
- **Docker 볼륨:** Docker가 관리하는 저장 공간을 컨테이너에 연결합니다.

| 구분 | 동작 방식 | 장점 | 고려 사항 |
|---|---|---|---|
| `COPY` | 빌드 시 파일을 이미지에 포함 | 이미지 자체로 배포 가능 | 소스 변경 시 이미지 재빌드 필요 |
| 바인드 마운트 | 호스트 경로를 컨테이너에 연결 | 개발 중 파일 변경 확인에 편리 | 호스트 경로와 권한에 영향받음 |
| Docker 볼륨 | Docker 관리 저장 공간을 연결 | 컨테이너를 교체해도 데이터 유지 가능 | 볼륨을 별도로 관리·백업해야 함 |

### 5) Docker Compose와 서비스 디스커버리

Docker Compose는 YAML 파일로 여러 컨테이너의 실행 설정을 관리합니다. 같은 Compose 프로젝트의 기본 네트워크에 연결된 서비스는 일반적으로 서비스 이름을 호스트 이름처럼 사용해 서로 통신할 수 있습니다.

예를 들어 `web` 서비스에서 `cache:6379`로 접근하면 Compose 네트워크의 `cache` 서비스에 연결을 시도합니다. 컨테이너 IP를 직접 지정하지 않아도 되므로 컨테이너가 재생성되어 IP가 바뀌는 상황에 대응하기 쉽습니다.

### 6) 환경 변수와 설정 분리

`.env` 파일에 `HOST_PORT=9090`을 정의하고 Compose 파일에서 `${HOST_PORT}`로 참조하면 포트 설정을 YAML 코드와 분리할 수 있습니다.

주의할 점은 Compose의 `.env`가 기본적으로 Compose 파일의 변수 치환에 사용된다는 것입니다. 컨테이너 내부 환경 변수로 전달하려면 서비스의 `environment` 또는 `env_file` 설정이 별도로 필요합니다.

### 7) Git 인증 방식과 보안

- HTTPS 인증은 환경에 따라 Personal Access Token(PAT), 자격 증명 관리자 등을 사용할 수 있습니다.
- SSH 인증은 공개키를 GitHub 계정에 등록하고 개인키로 인증합니다.
- 개인키는 공개 저장소에 올리지 않습니다.
- `.gitignore`는 Git 추적을 제외하고, `.dockerignore`는 Docker 빌드 컨텍스트에서 파일을 제외합니다. 두 파일의 역할은 서로 다릅니다.

---

## 🚀 6. 수행 내용 및 실행 로그

> 아래는 재현 가능한 명령어와 확인 기준입니다. 명령어를 다시 실행한 뒤 터미널에 실제로 표시된 결과를 필요한 위치에 기록합니다. 예시 출력이나 임의의 시간·ID를 실제 실행 결과인 것처럼 복사하지 않습니다.

### ① Git 설정 및 SSH 인증 확인

```powershell
# Git 사용자 설정 확인
git config --list

# 원격 저장소 주소 확인
git remote -v

# GitHub SSH 인증 테스트
ssh -T git@github.com

# 원격 저장소 주소를 SSH 형식으로 변경할 때
git remote set-url origin git@github.com:<사용자명>/<저장소명>.git

# 변경 결과 확인
git remote -v
```

**확인할 내용**

- `user.name`, `user.email`이 의도한 값인지 확인합니다.
- `git remote -v`의 fetch/push 주소가 SSH 형식인지 확인합니다.
- SSH 인증 성공 메시지가 표시되는지 확인합니다.
- GitHub는 SSH 인증 후 일반적인 셸 접속을 제공하지 않으므로, `successfully authenticated` 메시지는 인증 성공을 의미합니다.

> `git config --list` 결과에는 이메일 등 개인 정보가 포함될 수 있으므로 공개 README에 그대로 노출하지 않습니다.

### ② 터미널 기본 조작 및 파일 권한 변경

#### A. 디렉터리 생성과 위치 확인

WSL2 Ubuntu 터미널에서 실행합니다.

```bash
# 현재 위치 확인
pwd

# 작업 디렉터리 생성
mkdir -p ~/workspace/app

# 작업 디렉터리로 이동
cd ~/workspace

# 디렉터리 구조 확인
ls -la
```

#### B. 파일 생성·복사·이동·삭제

```bash
# 테스트 파일 생성
echo "CLI file operation test" > test.txt

# 파일 내용 확인
cat test.txt

# 파일 복사
cp test.txt test_copy.txt

# 복사된 파일 확인
ls -l test.txt test_copy.txt

# 파일 이동
mv test_copy.txt app/

# 이동 결과 확인
ls -l app/

# 이동한 파일 삭제
rm app/test_copy.txt

# 삭제 결과 확인
ls -l app/
```

**확인할 내용**

- `cp` 실행 후 원본과 복사본이 각각 존재하는지 확인합니다.
- `mv` 실행 후 파일이 목적지 디렉터리로 이동했는지 확인합니다.
- `rm` 실행 후 대상 파일이 목록에서 사라졌는지 확인합니다.

#### C. 권한 변경 전후 확인

Linux 파일 시스템 안에서 실행합니다.

```bash
# 실습 파일 생성
echo "Permission test" > app/index.html

# 변경 전 권한 확인
stat -c '%A %a %n' app/index.html

# 644 권한 적용
chmod 644 app/index.html

# 644 적용 결과 확인
stat -c '%A %a %n' app/index.html

# 755 권한 적용
chmod 755 app/index.html

# 755 적용 결과 확인
stat -c '%A %a %n' app/index.html
```

**확인 기준**

```text
644 적용: -rw-r--r-- 644 app/index.html
755 적용: -rwxr-xr-x 755 app/index.html
```

위 문자열은 Linux에서 해당 권한이 정상 적용됐을 때 기대하는 형식입니다. 실제 README의 실행 결과에는 본인 터미널에서 출력된 내용을 사용합니다.

> PowerShell에서 실행한 `chmod`와 `ls` 결과를 Linux 권한 변경의 증거로 사용하지 않습니다. WSL2에서 실행했다면 터미널 프롬프트와 현재 경로가 함께 보이도록 기록합니다.

### ③ Docker 설치 점검 및 기본 컨테이너 실행

PowerShell 또는 Docker Desktop과 연결된 터미널에서 실행합니다.

```powershell
# Docker CLI 버전 확인
docker --version

# Docker Engine 데몬 및 서버 정보 확인
docker info

# 테스트 컨테이너 실행
docker run --rm hello-world

# Ubuntu 컨테이너에서 기본 명령 실행
docker run --rm ubuntu:latest echo "Ubuntu container is working"
```

**확인할 내용**

- `docker --version`에서 클라이언트 버전을 확인합니다.
- `docker info`에서 Client뿐 아니라 Server 정보도 표시되는지 확인합니다.
- `hello-world` 컨테이너가 정상 실행되고 Docker 설치가 동작하는지 확인합니다.
- `--rm` 옵션은 컨테이너가 종료된 후 컨테이너를 자동 삭제합니다. 이미지까지 삭제하는 옵션은 아닙니다.

### ④ Dockerfile 작성 및 커스텀 이미지 빌드

프로젝트 루트에 `Dockerfile`을 작성합니다.

```dockerfile
FROM nginx:alpine

COPY app/ /usr/share/nginx/html/

EXPOSE 80
```

**명령어 실행**

```powershell
# 프로젝트 루트에서 이미지 빌드
docker build -t my-web:1.0 .

# 생성된 이미지 확인
docker images

# 컨테이너 실행
docker run -d --name web-test -p 8080:80 my-web:1.0

# 실행 중인 컨테이너와 포트 매핑 확인
docker ps

# 컨테이너 로그 확인
docker logs web-test

# 웹 서버 응답 확인
curl.exe http://localhost:8080

# 테스트 컨테이너 종료 및 삭제
docker rm -f web-test
```

**확인할 내용**

- 빌드가 완료되고 `my-web:1.0` 이미지가 생성되는지 확인합니다.
- `docker ps`의 PORTS 항목에서 호스트 8080번 포트와 컨테이너 80번 포트의 연결을 확인합니다.
- `curl.exe` 응답에 `app/index.html`의 내용이 표시되는지 확인합니다.
- `EXPOSE 80`은 이미지가 사용하는 포트를 문서화하는 설정이며, 호스트에 포트를 공개하는 기능은 `-p 8080:80`이 담당합니다.

### ⑤ 포트 매핑 및 브라우저 접속 확인

```powershell
# 컨테이너 실행
docker run -d --name web-test -p 8080:80 my-web:1.0

# 포트 매핑 확인
docker port web-test

# HTTP 응답 헤더 확인
curl.exe -I http://localhost:8080

# HTML 응답 내용 확인
curl.exe http://localhost:8080
```

브라우저에서 `http://localhost:8080`에 접속해 페이지가 표시되는지 확인합니다.

**확인할 내용**

- 브라우저 접속 성공은 호스트 포트에서 컨테이너의 NGINX까지 요청이 전달됐다는 의미입니다.
- 접속이 되지 않으면 컨테이너 상태, 포트 충돌, NGINX 로그를 순서대로 확인합니다.

### ⑥ 바인드 마운트 실시간 반영 확인

바인드 마운트는 호스트 디렉터리와 컨테이너 내부 디렉터리를 연결합니다. 개발 중 호스트 파일을 수정하고 컨테이너를 재빌드하지 않은 상태에서 변경을 확인할 때 유용합니다.

```powershell
# 기존 테스트 컨테이너가 있다면 정리
docker rm -f bind-test 2>$null

# 호스트 app 디렉터리를 컨테이너 웹 루트에 연결
docker run -d --name bind-test -p 8081:80 `
  --mount type=bind,source="${PWD}/app",target=/usr/share/nginx/html `
  nginx:alpine

# 컨테이너 실행 확인
docker ps

# 호스트 파일의 현재 내용 확인
Get-Content .\app\index.html

# 호스트 파일 내용 변경
Set-Content .\app\index.html '<h1>Bind Mount Test - Updated</h1>'

# 컨테이너 내부 파일 내용 확인
docker exec bind-test cat /usr/share/nginx/html/index.html

# 웹 서버 응답 확인
curl.exe http://localhost:8081
```

**확인할 내용**

- 호스트의 `app/index.html`을 수정한 뒤 컨테이너 내부 파일에도 변경 내용이 반영되는지 확인합니다.
- 브라우저 또는 `curl.exe`에서 변경된 HTML이 응답되는지 확인합니다.
- 바인드 마운트는 호스트 파일을 연결하므로 호스트 파일의 변경이 컨테이너에 보입니다. 반대로 컨테이너에서 파일을 수정하면 연결된 호스트 파일에도 영향을 줄 수 있으므로 주의합니다.

실습 종료:

```powershell
docker rm -f bind-test
```

### ⑦ Docker 볼륨 데이터 영속성 검증

Docker 볼륨은 컨테이너의 생명주기와 별도로 관리되는 저장 공간입니다. 컨테이너를 삭제한 뒤 새 컨테이너에 같은 볼륨을 연결해 데이터가 남아 있는지 확인합니다.

```powershell
# 볼륨 생성
docker volume create my_work_vol

# 볼륨을 연결한 테스트 컨테이너 실행
docker run -d --name vol-test `
  --mount source=my_work_vol,target=/data `
  ubuntu:latest sleep infinity

# 컨테이너 내부에 데이터 생성
docker exec vol-test bash -c "echo 'Persisted Data' > /data/memo.txt"

# 데이터 생성 여부 확인
docker exec vol-test cat /data/memo.txt

# 컨테이너 삭제
docker rm -f vol-test

# 새 임시 컨테이너에서 같은 볼륨의 데이터 확인
docker run --rm `
  --mount source=my_work_vol,target=/data `
  ubuntu:latest cat /data/memo.txt

# 볼륨 정보 확인
docker volume inspect my_work_vol
```

**확인할 내용**

- 첫 번째 컨테이너에서 `/data/memo.txt` 파일을 생성합니다.
- 해당 컨테이너를 삭제합니다.
- 새 컨테이너에 동일한 `my_work_vol`을 연결했을 때 기존 파일 내용이 출력되는지 확인합니다.
- 데이터가 유지되는 이유는 파일이 컨테이너의 임시 쓰기 계층이 아니라 Docker 볼륨에 저장됐기 때문입니다.

> `docker rm`은 컨테이너를 삭제하지만 일반적으로 명시적으로 삭제하지 않은 볼륨은 유지합니다. 볼륨 자체를 삭제하는 `docker volume rm`은 데이터가 사라질 수 있으므로 검증이 끝나기 전에는 실행하지 않습니다.

### ⑧ Docker Compose 멀티 컨테이너 구성

프로젝트 루트의 `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "${HOST_PORT:-9090}:80"
    volumes:
      - ./app:/usr/share/nginx/html:ro
    environment:
      APP_ENV: development
    depends_on:
      - cache

  cache:
    image: redis:alpine
```

`.env` 파일:

```env
HOST_PORT=9090
```

**설정 설명**

- `build: .`: 현재 디렉터리의 Dockerfile을 이용해 웹 이미지를 빌드합니다.
- `ports`: 호스트 포트와 컨테이너 80번 포트를 연결합니다.
- `volumes`: 호스트 `app/` 디렉터리를 NGINX 웹 루트에 읽기 전용으로 연결합니다.
- `environment`: 컨테이너 내부에 `APP_ENV` 환경 변수를 전달합니다.
- `depends_on`: `web` 서비스보다 `cache` 서비스를 먼저 시작하도록 실행 순서를 지정합니다. 단, 애플리케이션이 Redis의 준비 완료를 보장받는 헬스체크와 동일한 의미는 아닙니다.
- `cache`: Redis 컨테이너를 실행합니다. 같은 Compose 네트워크의 다른 서비스는 `cache`라는 서비스 이름으로 접근할 수 있습니다.

> NGINX 정적 파일을 컨테이너에서 수정할 필요가 없는 실습에서는 `:ro`를 붙여 읽기 전용으로 마운트할 수 있습니다. 호스트 파일 변경은 컨테이너에서 계속 확인할 수 있습니다.

### ⑨ Compose 실행 및 상태 확인

```powershell
# 이미지 빌드 및 서비스를 백그라운드로 실행
docker compose up -d --build

# 서비스 상태 확인
docker compose ps

# 전체 서비스 로그 확인
docker compose logs --tail=20

# web 서비스 로그 확인
docker compose logs --tail=20 web

# web 컨테이너에서 Redis 서비스 이름 해석 확인
docker compose exec web getent hosts cache

# web 컨테이너에서 Redis 포트 연결 확인
docker compose exec web sh -c "nc -zv cache 6379"

# 웹 서비스 응답 확인
curl.exe http://localhost:9090
```

**확인할 내용**

- `docker compose ps`에서 `web`, `cache` 서비스가 실행 중인지 확인합니다.
- `getent hosts cache`에서 서비스 이름 `cache`가 네트워크 주소로 해석되는지 확인합니다.
- `nc -zv cache 6379`에서 Redis 포트 연결이 성공하는지 확인합니다.
- `curl.exe`에서 웹 페이지의 HTML 응답이 반환되는지 확인합니다.

> `ping`은 이미지에 설치되어 있지 않을 수 있습니다. 서비스 이름 해석은 `getent hosts`, TCP 포트 연결은 `nc`로 확인하면 목적에 맞게 검증할 수 있습니다. `nc`도 이미지에 없으면 별도 설치가 필요할 수 있으므로, 실제 실행 환경에서 사용 가능한 명령어인지 먼저 확인합니다.

### ⑩ `.env` 포트 변경 확인

```powershell
# .env의 HOST_PORT 값을 9090으로 설정한 뒤 실행
docker compose up -d

# 실제 포트 매핑 확인
docker compose ps

# 웹 접속 확인
curl.exe http://localhost:9090
```

포트 변경 테스트를 진행할 때는 `.env`의 값을 예를 들어 `9091`로 바꾸고 다음을 실행합니다.

```powershell
docker compose up -d --force-recreate

# 변경된 포트 확인
docker compose ps

# 변경된 포트로 접속
curl.exe http://localhost:9091
```

**확인할 내용**

- `.env`의 `HOST_PORT` 값 변경이 Compose 포트 매핑에 반영되는지 확인합니다.
- 포트 매핑은 컨테이너 생성 설정이므로 값 변경 후 컨테이너 재생성이 필요할 수 있습니다.
- 테스트 후 제출용 기본 포트 값을 정리하고, README의 접속 주소도 실제 설정과 일치시킵니다.

### ⑪ Compose 종료 및 리소스 상태 확인

```powershell
# Compose 서비스 및 기본 네트워크 종료
docker compose down

# 실행 중인 컨테이너 확인
docker ps

# 남아 있는 이미지 확인
docker images
```

`docker compose down`은 Compose가 생성한 컨테이너와 기본 네트워크를 정리합니다. 별도로 생성한 Docker 볼륨은 기본적으로 유지됩니다. 볼륨까지 삭제하는 `docker compose down -v`는 데이터 삭제 위험이 있으므로 필요할 때만 사용합니다.

---

## 🚨 7. 트러블슈팅

### 1) Windows에서 chmod 결과가 바뀌지 않는 문제

**문제 상황**

PowerShell에서 `chmod 755 app/index.html`을 실행한 뒤 `ls` 결과의 `Mode`가 Linux의 `rwx` 형식으로 표시되지 않았습니다.

**원인**

PowerShell의 파일 목록 표시와 Windows 파일 권한 체계는 Linux의 `ls -l` 및 POSIX 권한 표기와 다릅니다. Windows 파일 시스템을 WSL에서 접근하는 경우에도 마운트 설정에 따라 권한 동작이 달라질 수 있습니다.

**해결 및 확인**

WSL2 Ubuntu의 Linux 파일 시스템 안에서 파일을 생성하고 `chmod`, `stat` 명령어로 변경 전후를 확인합니다.

```bash
cd ~/workspace
mkdir -p app
echo "Permission test" > app/index.html

stat -c '%A %a %n' app/index.html
chmod 644 app/index.html
stat -c '%A %a %n' app/index.html
chmod 755 app/index.html
stat -c '%A %a %n' app/index.html
```

### 2) 소스 수정 후 브라우저에 변경 사항이 반영되지 않는 문제

**문제 상황**

Dockerfile의 `COPY`로 이미지를 빌드한 뒤 호스트의 HTML 파일을 수정했지만, 기존 컨테이너의 웹 페이지에는 이전 내용이 표시될 수 있습니다.

**원인**

`COPY`는 이미지 빌드 시점의 파일을 이미지에 복사합니다. 이미 생성된 이미지나 컨테이너는 호스트 파일 변경을 자동으로 추적하지 않습니다.

**해결**

개발 중에는 바인드 마운트를 사용합니다.

```yaml
volumes:
  - ./app:/usr/share/nginx/html:ro
```

이후 호스트의 `app/index.html`을 수정하고 브라우저를 새로고침해 변경 사항을 확인합니다. 운영 배포에서는 변경된 소스를 포함해 이미지를 다시 빌드하는 방식을 고려합니다.

### 3) 포트 매핑 충돌

**문제 상황**

컨테이너 실행 시 `port is already allocated` 또는 `address already in use` 오류가 발생할 수 있습니다.

**원인 확인**

```powershell
docker ps
Get-NetTCPConnection -LocalPort 9090 -ErrorAction SilentlyContinue
```

**해결**

기존 컨테이너가 포트를 점유하고 있다면 해당 컨테이너를 종료하거나, `.env`의 `HOST_PORT`를 사용하지 않는 포트로 변경합니다.

```powershell
docker compose down
```

포트를 변경했다면 컨테이너를 재생성하고 새 포트로 접속되는지 확인합니다.

### 4) Compose 서비스 이름으로 통신할 수 없는 문제

**확인 순서**

```powershell
# 서비스 상태 확인
docker compose ps

# Compose 네트워크 확인
docker network ls

# web 컨테이너에서 서비스 이름 해석
docker compose exec web getent hosts cache

# Redis 포트 연결
docker compose exec web sh -c "nc -zv cache 6379"
```

**점검 사항**

- 두 서비스가 같은 Compose 네트워크에 연결되어 있는지 확인합니다.
- 서비스 이름이 실제 YAML의 서비스 키(`cache`)와 일치하는지 확인합니다.
- Redis 컨테이너가 실행 중인지 확인합니다.
- `depends_on`은 시작 순서를 지정할 뿐 서비스가 요청을 받을 준비가 끝났음을 항상 보장하지는 않습니다.

---

## 💡 8. 배운 점

- Linux 권한 표기인 `755`, `644`는 숫자별 권한 비트의 조합이며, Windows PowerShell의 파일 속성 표시와 구분해야 한다는 점을 이해했습니다.
- `COPY`는 빌드 시점에 파일을 이미지에 포함하고, 바인드 마운트는 호스트 파일을 컨테이너 경로에 연결한다는 차이를 확인했습니다.
- Docker 볼륨은 컨테이너와 별도로 데이터를 보관할 수 있어 컨테이너를 삭제하고 새로 생성해도 데이터를 유지할 수 있음을 실습했습니다.
- Docker Compose를 사용하면 여러 서비스의 실행 설정과 네트워크를 YAML 파일로 관리할 수 있음을 이해했습니다.
- 같은 Compose 네트워크에서는 서비스 이름을 이용해 컨테이너 간 통신을 시도할 수 있으며, 이름 해석과 TCP 포트 연결은 각각 별도로 확인할 수 있음을 배웠습니다.
- `.env`, `.gitignore`, `.dockerignore`는 각각 설정값 관리, Git 추적 제외, Docker 빌드 컨텍스트 제외라는 서로 다른 역할을 수행한다는 점을 정리했습니다.
- GitHub SSH 인증을 설정하면서 공개키와 개인키의 역할을 구분하고, 개인키와 민감 정보가 원격 저장소에 올라가지 않도록 관리해야 함을 확인했습니다.

---

## 📸 9. 실행 결과 스크린샷

현재 저장소에 포함된 스크린샷을 연결합니다. 이미지 파일이 실제로 존재하는지 확인한 뒤 파일명과 경로를 맞춰 사용합니다.

### Docker 빌드 수행 결과

![Docker build 성공](images/build.png)

### Docker Compose 서비스 상태 확인

![Docker Compose ps 성공](images/compose_ps.png)

### 브라우저 접속 결과

![브라우저 접속](images/browser.png)
