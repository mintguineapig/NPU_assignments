"""
4목 게임의 바둑판을 관리하는 Board 클래스
20x20 크기의 바둑판에서 돌을 놓고 승리 조건을 확인하는 기능을 제공합니다.
"""

class Board:
    def __init__(self, size=20):
        """
        바둑판을 초기화합니다. (기본값: 20x20)
        
        Args:
            size (int): 바둑판의 크기 (명세서 조건: 20x20)
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.EMPTY = 0
        self.PLAYER1 = 1  # 흑돌
        self.PLAYER2 = 2  # 백돌
    
    def display_board(self):
        """
        현재 바둑판 상태를 콘솔에 출력합니다. (바둑판 스타일 - 교차점에 돌 배치)
        """
        # 상단 열 번호 출력
        print("   ", end="")
        for i in range(self.size):
            print(f"{i:2}", end=" ")
        print()
        
        # 바둑판 격자 출력
        for i in range(self.size):
            # 행 번호 출력
            print(f"{i:2}:", end="")
            
            # 각 교차점과 선 출력
            for j in range(self.size):
                # 돌이 있는 경우 돌을 출력
                if self.board[i][j] == self.PLAYER1:
                    print(" ●", end="")
                elif self.board[i][j] == self.PLAYER2:
                    print(" ○", end="")
                else:
                    # 빈 교차점은 공백으로 표시
                    print("  ", end="")
                
                # 가로선 출력 (마지막 열이 아닌 경우)
                if j < self.size - 1:
                    print("─", end="")
            
            print()  # 줄바꿈
            
            # 세로선 출력 (마지막 행이 아닌 경우)
            if i < self.size - 1:
                print("   ", end="")
                for j in range(self.size):
                    print(" │", end="")
                    if j < self.size - 1:
                        print(" ", end="")
                print()
        
        print()
    
    def is_valid_move(self, row, col):
        """
        주어진 위치에 돌을 놓을 수 있는지 확인합니다.
        
        Args:
            row (int): 행 번호
            col (int): 열 번호
            
        Returns:
            bool: 유효한 위치이면 True, 아니면 False
        """
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == self.EMPTY)
    
    def place_stone(self, row, col, player):
        """
        지정된 위치에 돌을 놓습니다.
        
        Args:
            row (int): 행 번호
            col (int): 열 번호
            player (int): 플레이어 번호 (1 또는 2)
            
        Returns:
            bool: 성공적으로 돌을 놓았으면 True, 실패하면 False
        """
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self, row, col, player):
        """
        최근에 놓은 돌을 기준으로 승리 조건(4목)을 확인합니다.
        
        Args:
            row (int): 최근에 놓은 돌의 행 번호
            col (int): 최근에 놓은 돌의 열 번호
            player (int): 플레이어 번호
            
        Returns:
            bool: 승리 조건을 만족하면 True, 아니면 False
        """
        directions = [
            (0, 1),   # 가로
            (1, 0),   # 세로
            (1, 1),   # 대각선 (우하향)
            (1, -1)   # 대각선 (우상향)
        ]
        
        for dr, dc in directions:
            count = 1  # 현재 놓은 돌 포함
            
            # 한 방향으로 연속된 돌 개수 세기
            r, c = row + dr, col + dc
            while (0 <= r < self.size and 
                   0 <= c < self.size and 
                   self.board[r][c] == player):
                count += 1
                r, c = r + dr, c + dc
            
            # 반대 방향으로 연속된 돌 개수 세기
            r, c = row - dr, col - dc
            while (0 <= r < self.size and 
                   0 <= c < self.size and 
                   self.board[r][c] == player):
                count += 1
                r, c = r - dr, c - dc
            
            # 4개 이상 연속이면 승리
            if count >= 4:
                return True
        
        return False
    
    def is_board_full(self):
        """
        바둑판이 가득 찼는지 확인합니다.
        
        Returns:
            bool: 바둑판이 가득 찼으면 True, 아니면 False
        """
        for row in self.board:
            if self.EMPTY in row:
                return False
        return True
    
    def get_empty_positions(self):
        """
        비어있는 위치들의 리스트를 반환합니다.
        
        Returns:
            list: (row, col) 튜플들의 리스트
        """
        empty_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.EMPTY:
                    empty_positions.append((i, j))
        return empty_positions
    
    def copy(self):
        """
        현재 보드의 복사본을 만듭니다.
        
        Returns:
            Board: 현재 보드의 복사본
        """
        new_board = Board(self.size)
        for i in range(self.size):
            for j in range(self.size):
                new_board.board[i][j] = self.board[i][j]
        return new_board
