"""
4목 게임의 게임 로직을 관리하는 Game 클래스
플레이어 간의 턴 관리, 게임 진행, 승리 조건 확인을 담당합니다.
"""

from board import Board

class Game:
    def __init__(self):
        """
        게임을 초기화합니다. (20x20 바둑판)
        """
        self.board = Board(20)  # 명세서 조건: 20x20
        self.current_player = self.board.PLAYER1  # 흑돌부터 시작
        self.game_over = False
        self.winner = None
        self.player_names = {
            self.board.PLAYER1: "플레이어 1 (●)",
            self.board.PLAYER2: "플레이어 2 (○)"
        }
    
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
        print("          4목 게임 (Connect Four)")
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
        print("4목 게임을 시작합니다!")
        print("격자의 교차점에 4개의 돌을 연속으로 놓으면 승리합니다.")
        print("좌표는 '행 열' 형식으로 입력하세요 (예: 10 15)")
        print("게임을 종료하려면 'quit'을 입력하세요.")
        
        while not self.game_over:
            self.display_game_state()
            
            # 플레이어 입력 받기
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
