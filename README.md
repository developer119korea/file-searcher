# 파일 검색기 (File Searcher)

이 프로젝트는 사용자가 지정한 폴더 내에서 정규 표현식을 사용하여 파일을 검색하고, 검색된 파일을 목록으로 표시하는 간단한 파일 검색기 애플리케이션입니다. 또한, 검색된 파일을 선택하여 삭제하거나 Finder/Explorer에서 열 수 있는 기능을 제공합니다.

## 기능

- 폴더 선택
- 정규 표현식을 사용한 파일 검색
- 검색된 파일 목록 표시
- 파일 크기 및 생성 날짜 표시
- 파일 정렬 기능 (파일 경로, 크기, 생성 날짜 기준)
- 파일 선택 및 삭제
- Finder/Explorer에서 파일 보기

## 개발 환경

Python 3.12.6

## 설치 및 실행

1. 이 저장소를 클론합니다:

   ```bash
   git clone git@github.com:developer119korea/file-searcher.git
   cd file-searcher
   ```

2. 필요한 패키지를 설치합니다:

   ```bash
   pip install -r requirements.txt
   ```

3. 애플리케이션을 실행합니다:

   ```bash
   python main.py
   ```

## 사용 방법

1. 애플리케이션을 실행한 후, "Select Folder" 버튼을 클릭하여 검색할 폴더를 선택합니다.
2. "Regex" 입력 필드에 검색할 파일 이름 패턴을 정규 표현식으로 입력합니다.
3. "Preset" 드롭다운 메뉴에서 미리 정의된 정규 표현식을 선택할 수도 있습니다.
4. "Rescan" 버튼을 클릭하여 파일을 검색합니다.
5. 검색된 파일 목록이 테이블에 표시됩니다. 각 파일의 경로, 크기(MB), 생성 날짜가 표시됩니다.
6. 파일 목록에서 파일을 선택한 후, "Delete Selected Files" 버튼을 클릭하여 파일을 삭제할 수 있습니다.
7. 파일을 마우스 오른쪽 버튼으로 클릭하여 컨텍스트 메뉴에서 "View in Finder"를 선택하면 Finder/Explorer에서 파일을 볼 수 있습니다.

## 파일 구조

- `main.py`: 애플리케이션의 메인 코드가 포함된 파일입니다.
- `requirements.txt`: 필요한 패키지가 명시된 파일입니다.

## 기여

기여를 환영합니다! 버그를 발견하거나 개선 사항이 있다면 이슈를 생성해 주세요. 풀 리퀘스트도 환영합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.