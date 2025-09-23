# 4목 게임 (Connect Four)

20x20 바둑판에서 진행하는 4목 게임입니다. 사람끼리 플레이하거나 컴퓨터와 대전할 수 있습니다.

## 기능

1. **사람 vs 사람 모드**: 두 플레이어가 번갈아 가며 플레이
2. **사람 vs 컴퓨터 모드**: AI와 대전 (3단계 난이도)
3. **20x20 바둑판**: 넓은 바둑판에서 전략적 플레이
4. **승리 조건**: 가로, 세로, 대각선으로 4개 연속 배치

## 파일 구조

```
/root/2025_practice/
├── main.py                    # 메인 실행 파일
├── board.py                   # 바둑판 관리 클래스
├── game.py                    # 사람 vs 사람 게임 로직
├── game_with_ai.py           # 사람 vs 컴퓨터 게임 로직
├── ai_player.py              # AI 플레이어 클래스
├── flowchart_human_vs_human.md   # 사람 vs 사람 플로우차트
├── flowchart_human_vs_ai.md      # 사람 vs AI 플로우차트
└── README.md                 # 프로젝트 설명서
```

## 클래스 설계

### Board 클래스 (`board.py`)
- **역할**: 20x20 바둑판 관리
- **주요 메서드**:
  - `__init__(size)`: 바둑판 초기화
  - `display_board()`: 바둑판 출력
  - `is_valid_move(row, col)`: 유효한 움직임 확인
  - `place_stone(row, col, player)`: 돌 놓기
  - `check_winner(row, col, player)`: 승리 조건 확인
  - `is_board_full()`: 무승부 확인

### Game 클래스 (`game.py`)
- **역할**: 사람 vs 사람 게임 진행
- **주요 메서드**:
  - `play()`: 게임 메인 루프
  - `get_player_input()`: 플레이어 입력 처리
  - `make_move(row, col)`: 움직임 실행
  - `display_game_state()`: 게임 상태 출력

### GameWithAI 클래스 (`game_with_ai.py`)
- **역할**: 사람 vs 컴퓨터 게임 진행
- **주요 메서드**:
  - `play()`: AI 게임 메인 루프
  - `get_ai_move()`: AI 움직임 계산
  - `is_ai_turn()`: AI 차례 확인

### AIPlayer 클래스 (`ai_player.py`)
- **역할**: 인공지능 플레이어
- **알고리즘**: 미니맥스 + 알파-베타 가지치기
- **주요 메서드**:
  - `get_best_move(board)`: 최적의 수 계산
  - `minimax()`: 미니맥스 알고리즘
  - `evaluate_board()`: 보드 상태 평가
  - `find_immediate_win_or_block()`: 즉시 승부 확인

## 게임 실행

### 기본 실행
```bash
python3 main.py
```

### 메뉴 옵션
1. **플레이어 vs 플레이어**: 두 사람이 번갈아 플레이
2. **플레이어 vs 컴퓨터**: AI와 대전
   - 쉬움: 탐색 깊이 2
   - 보통: 탐색 깊이 3  
   - 어려움: 탐색 깊이 4
3. **게임 종료**: 프로그램 종료

### 게임 조작
- 돌 놓기: `행 열` 형식으로 입력 (예: `10 15`)
- 게임 종료: `quit` 입력
- 좌표 범위: 0~19

## AI 알고리즘 특징

### 미니맥스 알고리즘
- **목적**: 최적의 수 탐색
- **깊이 제한**: 성능과 품질의 균형
- **알파-베타 가지치기**: 탐색 공간 축소

### 평가 함수
- **4목 완성**: 1000점 (즉시 승리)
- **3목 + 빈칸**: 100점
- **2목 + 빈칸**: 10점
- **1목 + 빈칸**: 1점
- **중앙 위치 보너스**: 전략적 우위

### 최적화 기법
- 중앙 근처부터 우선 탐색
- 탐색 범위 제한 (최대 15-20개 위치)
- 즉시 승리/차단 수 우선 처리
- 보드 복사 최소화

## 플로우차트

### 사람 vs 사람 게임 흐름
자세한 내용은 `flowchart_human_vs_human.md` 참조

### 사람 vs AI 게임 흐름  
자세한 내용은 `flowchart_human_vs_ai.md` 참조

## 함수 단위 플로우차트

### 1. 메인 프로그램 흐름

```mermaid
graph TD
    A[main 함수 시작] --> B[show_menu 호출]
    B --> C[get_user_choice 호출]
    C --> D{사용자 선택}
    D -->|1| E[play_human_vs_human 호출]
    D -->|2| F[play_human_vs_ai 호출]
    D -->|3| G[프로그램 종료]
    E --> H[게임 완료 후 메뉴로 복귀]
    F --> H
    H --> B
```

### 2. Board 클래스 주요 함수

```mermaid
graph TD
    A[Board.__init__] --> B[20x20 배열 초기화]
    B --> C[플레이어 상수 설정]
    
    D[display_board] --> E[열 번호 출력]
    E --> F[격자와 돌 출력 루프]
    F --> G[교차점 표시 +]
    G --> H[돌 표시 ●○]
    
    I[is_valid_move] --> J{좌표 범위 확인}
    J -->|범위 내| K{빈 위치 확인}
    J -->|범위 외| L[False 반환]
    K -->|빈 위치| M[True 반환]
    K -->|돌 있음| L
    
    N[place_stone] --> O[is_valid_move 호출]
    O -->|유효| P[돌 배치]
    O -->|무효| Q[False 반환]
    P --> R[True 반환]
    
    S[check_winner] --> T[4방향 검사 시작]
    T --> U[각 방향별 연속 돌 개수 계산]
    U --> V{4개 이상 연속?}
    V -->|예| W[True 반환]
    V -->|아니오| X[다음 방향 검사]
    X --> Y{모든 방향 완료?}
    Y -->|아니오| U
    Y -->|예| Z[False 반환]
```

### 3. Game 클래스 주요 함수 (사람 vs 사람)

```mermaid
graph TD
    A[Game.play] --> B[게임 시작 메시지]
    B --> C{게임 종료?}
    C -->|아니오| D[display_game_state 호출]
    D --> E[get_player_input 호출]
    E --> F{입력 확인}
    F -->|quit| G[게임 종료]
    F -->|유효 좌표| H[make_move 호출]
    F -->|무효 입력| E
    H --> I{돌 놓기 성공?}
    I -->|성공| J[승리/무승부 확인]
    I -->|실패| E
    J --> K{게임 종료 조건?}
    K -->|종료| C
    K -->|계속| L[플레이어 교체]
    L --> C
    C -->|예| M[최종 결과 출력]
    
    N[get_player_input] --> O[사용자 입력 받기]
    O --> P{입력 형식 확인}
    P -->|quit| Q[quit 반환]
    P -->|좌표| R[좌표 파싱]
    P -->|잘못된 형식| S[에러 메시지]
    R --> T{좌표 범위 확인}
    T -->|유효| U[좌표 반환]
    T -->|무효| S
    S --> V[None 반환]
    
    W[make_move] --> X[is_valid_move 호출]
    X -->|무효| Y[에러 메시지, False 반환]
    X -->|유효| Z[place_stone 호출]
    Z --> AA[check_winner 호출]
    AA -->|승리| BB[게임 종료 설정]
    AA -->|계속| CC[is_board_full 호출]
    CC -->|가득참| DD[무승부 설정]
    CC -->|여유있음| EE[switch_player 호출]
    BB --> FF[True 반환]
    DD --> FF
    EE --> FF
```

### 4. GameWithAI 클래스 주요 함수 (사람 vs AI)

```mermaid
graph TD
    A[GameWithAI.play] --> B[게임 시작 메시지]
    B --> C{게임 종료?}
    C -->|아니오| D[display_game_state 호출]
    D --> E{AI 차례?}
    E -->|아니오| F[get_player_input 호출]
    E -->|예| G[get_ai_move 호출]
    F --> H{입력 처리}
    G --> I[make_move 호출]
    H -->|quit| J[게임 종료]
    H -->|유효| I
    H -->|무효| E
    I --> K{게임 종료 조건?}
    K -->|종료| C
    K -->|계속| E
    C -->|예| L[최종 결과 출력]
    
    M[get_ai_move] --> N[사고 중 메시지 출력]
    N --> O[ai_player.get_best_move 호출]
    O --> P[선택된 위치 출력]
    P --> Q[Enter 키 대기]
    Q --> R[선택된 좌표 반환]
    
    S[is_ai_turn] --> T{현재 플레이어 == PLAYER2?}
    T -->|예| U[True 반환]
    T -->|아니오| V[False 반환]
```

### 5. AIPlayer 클래스 주요 함수

```mermaid
graph TD
    A[get_best_move] --> B[find_immediate_win_or_block 호출]
    B --> C{즉시 승부 수 존재?}
    C -->|예| D[해당 수 반환]
    C -->|아니오| E{첫 번째 수?}
    E -->|예| F[중앙 위치 반환]
    E -->|아니오| G[가능한 수 목록 생성]
    G --> H[중앙 기준 정렬]
    H --> I[탐색 범위 제한]
    I --> J[각 수에 대해 minimax 호출]
    J --> K[최고 점수 수 선택]
    K --> L[선택된 수 반환]
    
    M[minimax] --> N{종료 조건 확인}
    N -->|depth=0| O[evaluate_board 반환]
    N -->|승리 발견| P[±1000 점수 반환]
    N -->|무승부| Q[0 반환]
    N -->|계속| R{Maximizing Player?}
    R -->|예| S[각 수에 대해 최대값 탐색]
    R -->|아니오| T[각 수에 대해 최소값 탐색]
    S --> U[Alpha-Beta 가지치기 적용]
    T --> U
    U --> V[최적 점수 반환]
    
    W[evaluate_board] --> X[모든 위치 순회]
    X --> Y[각 돌에 대해 evaluate_position 호출]
    Y --> Z{AI 돌인가?}
    Z -->|예| AA[점수 추가]
    Z -->|아니오| BB[점수 차감]
    AA --> CC[중앙 위치 보너스 계산]
    BB --> CC
    CC --> DD[총 점수 반환]
    
    EE[evaluate_position] --> FF[4방향 검사]
    FF --> GG[각 방향별 윈도우 생성]
    GG --> HH[evaluate_window 호출]
    HH --> II[점수 누적]
    II --> JJ{모든 방향 완료?}
    JJ -->|아니오| GG
    JJ -->|예| KK[총 점수 반환]
    
    LL[evaluate_window] --> MM[돌 개수 세기]
    MM --> NN{상대 돌 있음?}
    NN -->|예| OO[0점 반환]
    NN -->|아니오| PP{연속 돌 개수 확인}
    PP -->|4개| QQ[1000점 반환]
    PP -->|3개+빈칸| RR[100점 반환]
    PP -->|2개+빈칸| SS[10점 반환]
    PP -->|1개+빈칸| TT[1점 반환]
```

### 6. 전체 시스템 통합 플로우

```mermaid
graph TD
    A[프로그램 시작] --> B[main 함수]
    B --> C[메뉴 표시 루프]
    C --> D{게임 모드 선택}
    D -->|사람vs사람| E[Game 객체 생성]
    D -->|사람vs AI| F[GameWithAI 객체 생성]
    D -->|종료| G[프로그램 종료]
    
    E --> H[사람vs사람 게임 루프]
    H --> I[플레이어 입력]
    I --> J[보드 업데이트]
    J --> K[승리 확인]
    K --> L{게임 종료?}
    L -->|아니오| M[플레이어 교체]
    M --> H
    L -->|예| N[결과 출력]
    
    F --> O[사람vs AI 게임 루프]
    O --> P{현재 차례?}
    P -->|사람| Q[사용자 입력 처리]
    P -->|AI| R[AI 수 계산]
    Q --> S[보드 업데이트]
    R --> T[AI 수 실행]
    T --> S
    S --> U[승리 확인]
    U --> V{게임 종료?}
    V -->|아니오| W[차례 교체]
    W --> O
    V -->|예| X[결과 출력]
    
    N --> Y[재시작 확인]
    X --> Y
    Y --> Z{재시작?}
    Z -->|예| AA[게임 리셋]
    Z -->|아니오| C
    AA --> H
    AA --> O
```

## 게임 규칙

1. **목표**: 가로, 세로, 대각선 중 하나로 4개의 돌을 연속 배치
2. **플레이어**: 흑돌(●)과 백돌(○)
3. **차례**: 흑돌부터 시작하여 번갈아 진행
4. **승리**: 4개 연속 배치한 플레이어 승리
5. **무승부**: 바둑판이 가득 찰 때까지 승부가 나지 않으면 무승부

## 개발 환경

- **언어**: Python 3.13
- **의존성**: 표준 라이브러리만 사용
- **운영체제**: Linux (Debian)

## 실행 예시

```bash
$ python3 main.py

==================================================
          4목 게임 (Connect Four)
==================================================
1. 플레이어 vs 플레이어
2. 플레이어 vs 컴퓨터
3. 게임 종료
==================================================
선택하세요 (1-3): 2

컴퓨터 난이도를 선택하세요:
1. 쉬움 (탐색 깊이: 2)
2. 보통 (탐색 깊이: 3)
3. 어려움 (탐색 깊이: 4)
난이도 선택 (1-3): 2

4목 게임을 시작합니다! (사람 vs 컴퓨터)
...
```

이제 모든 조건을 만족하는 4목 게임이 완성되었습니다!
