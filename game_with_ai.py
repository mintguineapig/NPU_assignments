"""
AI가 포함된 4목 게임 클래스
사람과 컴퓨터가 플레이할 수 있는 게임 로직을 제공합니다.
"""

from board import Board
from ai_player import AIPlayer
import time

class GameWithAI:
    def __init__(self):
        """
        AI가 포함된 게임을 초기화합니다. (20x20 바둑판, 기본 난이도)
        """
        self.board = Board(20)  # 명세서 조건: 20x20
        self.current_player = self.board.PLAYER1  # 사람이 먼저 시작
        self.game_over = False
        self.winner = None
        self.ai_player = AIPlayer(self.board.PLAYER2, 3)  # AI는 플레이어 2, 기본 난이도
        self.player_names = {
            self.board.PLAYER1: "플레이어 (●)",
            self.board.PLAYER2: "컴퓨터 (○)"
        }
        self.thinking_time = 1.0  # AI 사고 시간 (시각적 효과)
    
    def get_current_player_name(self):
        """
        현재 플레이어의 이름을 반환합니다.
        
        Returns:
            str: 현재 플레이어의 이름
        """
        return self.player_names[self.current_player]
    
    def get_winner_name(self):
        """
        승리한 플레이어의 이름을 반환합니다.
        
        Returns:
            str: 승리한 플레이어의 이름, 무승부면 "무승부"
        """
        if self.winner:
            return self.player_names[self.winner]
        elif self.game_over:
            return "무승부"
        return None
    
    def switch_player(self):
        """
        현재 플레이어를 다음 플레이어로 바꿉니다.
        """
        self.current_player = (self.board.PLAYER2 
                              if self.current_player == self.board.PLAYER1 
                              else self.board.PLAYER1)
    
    def is_ai_turn(self):
        """
        현재 AI의 차례인지 확인합니다.
        
        Returns:
            bool: AI의 차례이면 True
        """
        return self.current_player == self.board.PLAYER2
    
    def get_player_input(self):
        """
        플레이어로부터 입력을 받습니다.
        
        Returns:
            tuple: (row, col) 또는 None (잘못된 입력)
        """
        try:
            print(f"\n{self.get_current_player_name()}의 차례입니다.")
            print("돌을 놓을 위치를 입력하세요 (예: 10 15) 또는 'quit'으로 종료:")
            
            user_input = input().strip()
            
            if user_input.lower() == 'quit':
                return 'quit'
            
            parts = user_input.split()
            if len(parts) != 2:
                print("잘못된 입력입니다. 행과 열을 공백으로 구분하여 입력하세요.")
                return None
            
            row, col = int(parts[0]), int(parts[1])
            
            if not (0 <= row < self.board.size and 0 <= col < self.board.size):
                print(f"입력 범위를 벗어났습니다. 0~{self.board.size-1} 사이의 값을 입력하세요.")
                return None
            
            return (row, col)
            
        except ValueError:
            print("숫자를 입력하세요.")
            return None
        except KeyboardInterrupt:
            return 'quit'
    
    def get_ai_move(self):
        """
        AI의 최적의 수를 계산합니다.
        
        Returns:
            tuple: (row, col) AI가 선택한 위치
        """
        print(f"\n{self.get_current_player_name()}이 생각 중입니다...")
        
        # 시각적 효과를 위한 대기
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(self.thinking_time / 3)
        print(" 완료!")
        
        # AI의 최적 수 계산
        move = self.ai_player.get_best_move(self.board)
        
        if move:
            row, col = move
            print(f"컴퓨터가 ({row}, {col})에 돌을 놓았습니다.")
            print("Enter 키를 눌러 계속...")
            input()  # 사용자가 결과를 확인할 수 있도록 대기
        
        return move
    
    def make_move(self, row, col):
        """
        지정된 위치에 현재 플레이어의 돌을 놓습니다.
        
        Args:
            row (int): 행 번호
            col (int): 열 번호
            
        Returns:
            bool: 성공적으로 돌을 놓았으면 True, 실패하면 False
        """
        if not self.board.is_valid_move(row, col):
            if not self.is_ai_turn():  # 사람 플레이어에게만 에러 메시지 표시
                print("이미 돌이 놓여있거나 잘못된 위치입니다.")
            return False
        
        # 돌 놓기
        self.board.place_stone(row, col, self.current_player)
        
        # 승리 조건 확인
        if self.board.check_winner(row, col, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            return True
        
        # 무승부 확인
        if self.board.is_board_full():
            self.game_over = True
            return True
        
        # 플레이어 교체
        self.switch_player()
        return True
    
    def display_game_state(self):
        """
        현재 게임 상태를 화면에 출력합니다.
        """
        print("\n" + "="*50)
        print("       4목 게임 (사람 vs 컴퓨터)")
        print("="*50)
        self.board.display_board()
        
        if not self.game_over:
            print(f"현재 차례: {self.get_current_player_name()}")
        else:
            winner_name = self.get_winner_name()
            if winner_name == "무승부":
                print("게임이 무승부로 끝났습니다!")
            else:
                print(f"🎉 {winner_name}이(가) 승리했습니다! 🎉")
    
    def play(self):
        """
        게임을 시작하고 진행합니다.
        """
        print("4목 게임을 시작합니다! (사람 vs 컴퓨터)")
        print("격자의 교차점에 4개의 돌을 연속으로 놓으면 승리합니다.")
        print("좌표는 '행 열' 형식으로 입력하세요 (예: 10 15)")
        print("게임을 종료하려면 'quit'을 입력하세요.")
        print("플레이어가 흑돌(●), 컴퓨터가 백돌(○)입니다.")
        
        while not self.game_over:
            self.display_game_state()
            
            if self.is_ai_turn():
                # AI의 차례
                move = self.get_ai_move()
                if move is None:
                    print("AI가 유효한 수를 찾지 못했습니다.")
                    break
                
                row, col = move
                if not self.make_move(row, col):
                    print("AI가 잘못된 수를 선택했습니다.")
                    break
            else:
                # 사람 플레이어의 차례
                move = self.get_player_input()
                
                if move == 'quit':
                    print("게임을 종료합니다.")
                    return
                
                if move is None:
                    continue  # 잘못된 입력이면 다시 입력받기
                
                row, col = move
                
                # 움직임 실행
                if not self.make_move(row, col):
                    continue  # 잘못된 움직임이면 다시 입력받기
        
        # 게임 종료 후 최종 상태 출력
        self.display_game_state()
    
    def reset_game(self):
        """
        게임을 초기 상태로 재설정합니다.
        """
        self.board = Board(20)  # 명세서 조건: 20x20
        self.current_player = self.board.PLAYER1
        self.game_over = False
        self.winner = None
