"""
4목 게임 메인 실행 파일
사용자가 게임 모드를 선택하고 게임을 실행할 수 있습니다.
"""

from game import Game
from game_with_ai import GameWithAI

def show_menu():
    """
    게임 메뉴를 표시합니다.
    """
    print("\n" + "="*50)
    print("          4목 게임 (Connect Four)")
    print("="*50)
    print("1. 플레이어 vs 플레이어")
    print("2. 플레이어 vs 컴퓨터")
    print("3. 게임 종료")
    print("="*50)

def get_user_choice():
    """
    사용자의 메뉴 선택을 받습니다.
    
    Returns:
        str: 사용자가 선택한 메뉴 번호
    """
    while True:
        try:
            choice = input("선택하세요 (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            else:
                print("1, 2, 또는 3을 입력하세요.")
        except KeyboardInterrupt:
            return '3'

def play_human_vs_human():
    """
    사람 vs 사람 게임을 실행합니다.
    """
    game = Game()
    
    while True:
        game.play()
        
        # 게임 종료 후 재시작 여부 확인
        while True:
            try:
                again = input("\n다시 게임하시겠습니까? (y/n): ").strip().lower()
                if again in ['y', 'yes', '예']:
                    game.reset_game()
                    break
                elif again in ['n', 'no', '아니오']:
                    return
                else:
                    print("y 또는 n을 입력하세요.")
            except KeyboardInterrupt:
                return

def play_human_vs_ai():
    """
    사람 vs AI 게임을 실행합니다.
    """
    game = GameWithAI()
    
    while True:
        game.play()
        
        # 게임 종료 후 재시작 여부 확인
        while True:
            try:
                again = input("\n다시 게임하시겠습니까? (y/n): ").strip().lower()
                if again in ['y', 'yes', '예']:
                    game.reset_game()
                    break
                elif again in ['n', 'no', '아니오']:
                    return
                else:
                    print("y 또는 n을 입력하세요.")
            except KeyboardInterrupt:
                return
    """
    사람 vs 사람 게임을 실행합니다.
    """
    game = Game()
    
    while True:
        game.play()
        
        # 게임 종료 후 재시작 여부 확인
        while True:
            try:
                again = input("\n다시 게임하시겠습니까? (y/n): ").strip().lower()
                if again in ['y', 'yes', '예']:
                    game.reset_game()
                    break
                elif again in ['n', 'no', '아니오']:
                    return
                else:
                    print("y 또는 n을 입력하세요.")
            except KeyboardInterrupt:
                return

def main():
    """
    메인 함수 - 프로그램의 진입점입니다.
    """
    print("4목 게임에 오신 것을 환영합니다!")
    
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice == '1':
            play_human_vs_human()
        elif choice == '2':
            play_human_vs_ai()
        elif choice == '3':
            print("게임을 종료합니다. 안녕히 가세요!")
            break

if __name__ == "__main__":
    main()
