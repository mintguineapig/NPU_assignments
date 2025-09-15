# 4목 게임 플로우차트 (사람 vs 사람)

## << Mermaid flow chart >>

## 사용자가 메뉴에서 2번 선택 후 Function Flow

```mermaid
flowchart TD
    A[사용자가 메뉴에서 2 선택] --> B[play_human_vs_ai 함수 호출]
    B --> C[GameWithAI 객체 생성]
    C --> D[GameWithAI.__init__]
    D --> E[Board 객체 생성]
    E --> F[AIPlayer 객체 생성]
    F --> G[게임 시작 메시지 출력]
    G --> H[game.play 함수 호출]
    
    H --> I[게임 루프 시작]
    I --> J[board.display_board 호출]
    J --> K{현재 플레이어가 AI인가?}
    
    K -->|No - Human 턴| L[get_player_input 호출]
    L --> M[사용자 입력 받기]
    M --> N{입력이 'quit'인가?}
    N -->|Yes| O[게임 종료]
    N -->|No| P[입력 파싱 및 검증]
    P --> Q[board.is_valid_move 호출]
    Q --> R{유효한 입력인가?}
    R -->|No| S[오류 메시지 출력]
    S --> L
    R -->|Yes| T[make_move 호출]
    
    K -->|Yes - AI 턴| U[get_ai_move 호출]
    U --> V[AI 사고 중 메시지 출력]
    V --> W[ai_player.get_best_move 호출]
    W --> X[find_immediate_win_or_block 호출]
    X --> Y{즉시 승부수가 있는가?}
    Y -->|Yes| Z[즉시수 반환]
    Y -->|No| AA[minimax 알고리즘 시작]
    AA --> BB[get_possible_moves 호출]
    BB --> CC[sort_moves_by_center 호출]
    CC --> DD[각 가능한 수에 대해 minimax 호출]
    DD --> EE[evaluate_board 호출]
    EE --> FF[최적수 계산 완료]
    FF --> GG[AI 선택한 위치 출력]
    Z --> HH[make_move 호출]
    GG --> HH
    
    T --> II[board.place_stone 호출]
    HH --> II
    II --> JJ[board.display_board 호출]
    JJ --> KK[board.check_winner 호출]
    KK --> LL{승자가 있는가?}
    LL -->|No| MM[플레이어 변경]
    MM --> K
    LL -->|Yes| NN[승자 발표]
    NN --> OO[게임 종료]
    
    O --> PP{다시 게임하겠는가?}
    OO --> PP
    PP -->|Yes| QQ[game.reset_game 호출]
    QQ --> H
    PP -->|No| RR[play_human_vs_ai 함수 종료]
    RR --> SS[main 함수로 복귀]
    SS --> TT[show_menu 다시 호출]
```

## AI 함수 상세 호출 플로우

```mermaid
flowchart TD
    A[ai_player.get_best_move 호출] --> B[find_immediate_win_or_block 호출]
    B --> C{AI 승리 가능한 수 있는가?}
    C -->|Yes| D[승리수 반환]
    C -->|No| E{상대 승리 차단 필요한가?}
    E -->|Yes| F[차단수 반환]
    E -->|No| G[get_possible_moves 호출]
    
    G --> H[sort_moves_by_center 호출]
    H --> I[limit_search_moves 호출]
    I --> J[best_score = -무한대]
    J --> K[각 가능한 수에 대해 반복]
    
    K --> L[board 복사]
    L --> M[test_move 놓기]
    M --> N[minimax 재귀 호출]
    N --> O{maximizing_player?}
    
    O -->|Yes| P[모든 자식 노드 탐색]
    P --> Q[max_eval 계산]
    Q --> R[alpha 업데이트]
    R --> S{alpha >= beta?}
    S -->|Yes| T[가지치기 - break]
    S -->|No| U{더 탐색할 수 있는가?}
    U -->|Yes| P
    U -->|No| V[max_eval 반환]
    
    O -->|No| W[모든 자식 노드 탐색]
    W --> X[min_eval 계산]
    X --> Y[beta 업데이트]
    Y --> Z{beta <= alpha?}
    Z -->|Yes| AA[가지치기 - break]
    Z -->|No| BB{더 탐색할 수 있는가?}
    BB -->|Yes| W
    BB -->|No| CC[min_eval 반환]
    
    V --> DD[score와 best_score 비교]
    CC --> DD
    T --> DD
    AA --> DD
    DD --> EE{새로운 best_score인가?}
    EE -->|Yes| FF[best_move 업데이트]
    EE -->|No| GG{더 많은 수가 있는가?}
    FF --> GG
    GG -->|Yes| K
    GG -->|No| HH[best_move 반환]
    
    D --> II[선택된 수 반환]
    F --> II
    HH --> II
```

## 게임 초기화 및 객체 생성 플로우

```mermaid
flowchart TD
    A[play_human_vs_ai 호출] --> B[GameWithAI 생성자 호출]
    B --> C[Board 객체 생성]
    C --> D[Board.__init__]
    D --> E[20x20 빈 보드 초기화]
    E --> F[AIPlayer 객체 생성]
    F --> G[AIPlayer.__init__]
    G --> H[AI 플레이어 번호 설정]
    H --> I[current_player = 1 설정]
    I --> J[game_over = False 설정]
    J --> K[초기화 완료]
    K --> L[게임 시작 메시지]
    L --> M[game.play 호출]
```

## 턴 관리 및 플레이어 변경 플로우

```mermaid
flowchart TD
    A[턴 시작] --> B{current_player == 1?}
    B -->|Yes| C[Human 플레이어 턴]
    B -->|No| D[AI 플레이어 턴]
    
    C --> E[get_player_input 호출]
    E --> F[사용자 입력 처리]
    F --> G[make_move 호출]
    
    D --> H[get_ai_move 호출]
    H --> I[AI 수 계산]
    I --> J[make_move 호출]
    
    G --> K[돌 배치 완료]
    J --> K
    K --> L[승리 조건 확인]
    L --> M{게임 종료?}
    M -->|No| N[플레이어 변경]
    N --> O{current_player == 1?}
    O -->|Yes| P[current_player = 2]
    O -->|No| Q[current_player = 1]
    P --> B
    Q --> B
    M -->|Yes| R[게임 종료 처리]
```









## 1. 메인 함수 플로우

```
main()
├── show_menu() → 메뉴 출력
├── get_user_choice() → 사용자 선택 입력
└── 선택에 따라 분기
    ├── 1: play_human_vs_human() 호출
    └── 2: 프로그램 종료
```

## 2. 게임 실행 플로우

```
play_human_vs_human()
├── Game() 객체 생성
├── game.play() 호출
├── 게임 종료 후 재시작 여부 확인
└── 사용자 선택에 따라 분기
    ├── 재시작: game.reset_game() → 반복
    └── 종료: 함수 종료
```

## 3. 게임 진행 플로우

```
Game.play()
├── 게임 시작 메시지 출력
└── 게임 루프 (while not game_over)
    ├── display_game_state() → 현재 게임 상태 출력
    ├── get_player_input() → 플레이어 입력 받기
    │   ├── 'quit' 입력시 → 게임 종료
    │   ├── 잘못된 입력시 → None 반환, 다시 입력
    │   └── 유효한 입력시 → (row, col) 반환
    ├── make_move(row, col) → 돌 놓기
    │   ├── 유효하지 않은 위치 → False 반환, 다시 입력
    │   └── 유효한 위치 → True 반환, 게임 계속
    └── 게임 종료 조건 확인
        ├── 승리 조건 만족 → game_over = True, winner 설정
        ├── 보드 가득참 → game_over = True (무승부)
        └── 계속 진행 → 플레이어 교체
```

## 4. 돌 놓기 플로우

```
Game.make_move(row, col)
├── Board.is_valid_move(row, col) → 유효성 검사
│   └── False → 에러 메시지, False 반환
├── Board.place_stone(row, col, current_player) → 돌 놓기
├── Board.check_winner(row, col, current_player) → 승리 조건 확인
│   └── True → game_over = True, winner = current_player
├── Board.is_board_full() → 무승부 확인
│   └── True → game_over = True
└── switch_player() → 플레이어 교체
```

## 5. 승리 조건 확인 플로우

```
Board.check_winner(row, col, player)
├── 4방향 검사 (가로, 세로, 대각선)
│   ├── 각 방향에 대해:
│   │   ├── 현재 위치에서 한 방향으로 연속 돌 개수 세기
│   │   ├── 현재 위치에서 반대 방향으로 연속 돌 개수 세기
│   │   └── 총 개수 = 1 + 양방향 개수
│   └── 총 개수 >= 4 → True 반환
└── 모든 방향 검사 완료 → False 반환
```

## 6. 보드 관리 플로우

```
Board 클래스 주요 메서드:
├── __init__(size) → 보드 초기화
├── display_board() → 보드 상태 출력
├── is_valid_move(row, col) → 유효한 움직임 확인
├── place_stone(row, col, player) → 돌 놓기
├── check_winner(row, col, player) → 승리 조건 확인
├── is_board_full() → 보드 가득참 확인
├── get_empty_positions() → 빈 위치 반환
└── copy() → 보드 복사
```

## 7. 전체 시스템 플로우

```
시작
├── main() 함수 실행
├── 사용자 메뉴 선택
├── 게임 모드 선택 (현재는 사람 vs 사람만)
├── Game 객체 생성 및 초기화
├── 게임 루프 시작
│   ├── 현재 게임 상태 표시
│   ├── 현재 플레이어 입력 받기
│   ├── 입력 유효성 검사
│   ├── 돌 놓기 및 승리 조건 확인
│   ├── 게임 종료 조건 확인
│   └── 플레이어 교체
├── 게임 결과 표시
├── 재시작 여부 확인
└── 프로그램 종료 또는 재시작
```
