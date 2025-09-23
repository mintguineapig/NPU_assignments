"""
4목 게임의 AI 플레이어 클래스
미니맥스 알고리즘과 알파-베타 가지치기를 사용하여 최적의 수를 찾습니다.
"""
import math
import random
from board import Board

class AIPlayer:
    def __init__(self, player_number, difficulty=3):
        """
        AI 플레이어를 초기화합니다.
        
        Args:
            player_number (int): AI 플레이어 번호 (1 또는 2)
            difficulty (int): 탐색 깊이 (고정값: 3 - 최고 실력)
        """
        self.player = player_number
        self.opponent = 2 if player_number == 1 else 1
        self.max_depth = difficulty
        
    def evaluate_position(self, board, row, col, player, length):
        """
        특정 위치에서 주어진 길이의 연속된 돌을 평가합니다.
        
        Args:
            board: 게임 보드
            row, col: 평가할 위치
            player: 플레이어 번호
            length: 평가할 연속 길이
            
        Returns:
            int: 해당 위치의 점수
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 가로, 세로, 대각선
        
        for dr, dc in directions:
            # 한 방향으로 length만큼의 윈도우를 확인
            for start in range(-length + 1, 1):
                window = []
                valid_window = True
                
                for i in range(length):
                    r = row + start * dr + i * dr
                    c = col + start * dc + i * dc
                    
                    if 0 <= r < board.size and 0 <= c < board.size:
                        window.append(board.board[r][c])
                    else:
                        valid_window = False
                        break
                
                if valid_window:
                    score += self.evaluate_window(window, player)
        
        return score
    
    def evaluate_window(self, window, player):
        """
        4개 길이의 윈도우를 평가하여 점수를 반환합니다.
        
        Args:
            window (list): 4개 위치의 상태 리스트
            player (int): 평가할 플레이어 번호
            
        Returns:
            int: 윈도우의 점수
        """
        score = 0
        opponent = 2 if player == 1 else 1
        
        player_count = window.count(player)
        empty_count = window.count(0)
        opponent_count = window.count(opponent)
        
        # 상대방이 있으면 이 윈도우는 무효
        if opponent_count > 0:
            return 0
        
        # 연속된 돌의 개수에 따른 점수
        if player_count == 4:
            score += 1000  # 승리
        elif player_count == 3 and empty_count == 1:
            score += 100   # 3목
        elif player_count == 2 and empty_count == 2:
            score += 10    # 2목
        elif player_count == 1 and empty_count == 3:
            score += 1     # 1목
        
        return score
    
    def evaluate_board(self, board):
        """
        전체 보드를 평가하여 점수를 반환합니다.
        
        Args:
            board: 게임 보드
            
        Returns:
            int: 보드의 전체 점수
        """
        score = 0
        
        # 모든 위치에 대해 평가
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] != 0:
                    player = board.board[row][col]
                    position_score = self.evaluate_position(board, row, col, player, 4)
                    
                    if player == self.player:
                        score += position_score
                    else:
                        score -= position_score
        
        # 중앙 근처에 더 높은 가중치 부여
        center = board.size // 2
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] == self.player:
                    distance_from_center = abs(row - center) + abs(col - center)
                    score += max(0, 10 - distance_from_center)
        
        return score
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        미니맥스 알고리즘과 알파-베타 가지치기를 사용하여 최적의 수를 찾습니다.
        
        Args:
            board: 게임 보드
            depth: 탐색 깊이
            alpha: 알파 값 (알파-베타 가지치기)
            beta: 베타 값 (알파-베타 가지치기)
            maximizing_player: 최대화 플레이어인지 여부
            
        Returns:
            int: 보드의 평가 점수
        """
        # 종료 조건 확인
        if depth == 0:
            return self.evaluate_board(board)
        
        # 승리 조건 확인
        for row in range(board.size):
            for col in range(board.size):
                if board.board[row][col] != 0:
                    player = board.board[row][col]
                    if board.check_winner(row, col, player):
                        if player == self.player:
                            return 1000 + depth  # AI 승리
                        else:
                            return -1000 - depth  # AI 패배
        
        # 무승부 확인
        if board.is_board_full():
            return 0
        
        # 가능한 수들 중에서 중앙 근처부터 우선 탐색
        empty_positions = board.get_empty_positions()
        center = board.size // 2
        empty_positions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
        
        # 탐색 범위 제한 (성능 최적화)
        if len(empty_positions) > 20:
            empty_positions = empty_positions[:20]
        
        if maximizing_player:
            max_eval = -math.inf
            for row, col in empty_positions:
                board.place_stone(row, col, self.player)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.board[row][col] = 0  # 되돌리기
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # 베타 컷오프
            
            return max_eval
        else:
            min_eval = math.inf
            for row, col in empty_positions:
                board.place_stone(row, col, self.opponent)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.board[row][col] = 0  # 되돌리기
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # 알파 컷오프
            
            return min_eval
    
    def find_immediate_win_or_block(self, board):
        """
        즉시 승리할 수 있는 수나 상대방의 승리를 막는 수를 찾습니다.
        
        Args:
            board: 게임 보드
            
        Returns:
            tuple: (row, col) 또는 None
        """
        empty_positions = board.get_empty_positions()
        
        # 1. 즉시 승리할 수 있는 수 찾기
        for row, col in empty_positions:
            board.place_stone(row, col, self.player)
            if board.check_winner(row, col, self.player):
                board.board[row][col] = 0  # 되돌리기
                return (row, col)
            board.board[row][col] = 0  # 되돌리기
        
        # 2. 상대방의 승리를 막는 수 찾기
        for row, col in empty_positions:
            board.place_stone(row, col, self.opponent)
            if board.check_winner(row, col, self.opponent):
                board.board[row][col] = 0  # 되돌리기
                return (row, col)
            board.board[row][col] = 0  # 되돌리기
        
        return None
    
    def get_best_move(self, board):
        """
        현재 보드 상태에서 최적의 수를 반환합니다.
        
        Args:
            board: 게임 보드
            
        Returns:
            tuple: (row, col) 최적의 위치
        """
        # 1. 즉시 승리하거나 상대방을 막는 수가 있는지 확인
        immediate_move = self.find_immediate_win_or_block(board)
        if immediate_move:
            return immediate_move
        
        # 2. 미니맥스 알고리즘으로 최적의 수 찾기
        empty_positions = board.get_empty_positions()
        
        if not empty_positions:
            return None
        
        # 첫 번째 수는 중앙 근처에서 시작
        if len(empty_positions) == board.size * board.size:
            center = board.size // 2
            return (center, center)
        
        # 중앙 근처부터 우선 탐색
        center = board.size // 2
        empty_positions.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
        
        # 탐색 범위 제한 (성능 최적화)
        if len(empty_positions) > 15:
            empty_positions = empty_positions[:15]
        
        best_move = None
        best_score = -math.inf
        
        for row, col in empty_positions:
            # 보드 복사본에서 테스트
            test_board = board.copy()
            test_board.place_stone(row, col, self.player)
            
            score = self.minimax(test_board, self.max_depth - 1, 
                               -math.inf, math.inf, False)
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move if best_move else random.choice(empty_positions)
