import random
import math

# 초기 설정
TEAM_SIZE = 5
TOTAL_TEAMS = 5
STARTING_COINS = 10

class Player:
    def __init__(self, name, team_id, is_user=False):
        self.name = name
        self.team_id = team_id
        self.coins = 0
        self.reputation = 0
        self.dao_tickets = 1
        self.is_user = is_user
        self.burned_tickets = False

    def receive_coins(self):
        # 플레이어가 선택하여 코인 10개를 받는 경우
        self.coins += 10

    def add_to_bank(self):
        # 외부에서 팀 은행에 1~5 코인 추가
        return random.randint(1, 5)

    def vote_power(self):
        # 평판 점수의 제곱근을 반올림한 값이 투표권 개수, 최소 1개 보장
        return max(1, round(math.sqrt(self.reputation)))

    def burn_ticket(self, team_bank, total_tickets):
        if not self.burned_tickets and self.dao_tickets > 0:
            reward = team_bank / total_tickets
            self.coins += reward
            self.dao_tickets -= 1
            self.burned_tickets = True
            print(f"{self.name}가 DAO 티켓을 태워 {reward:.2f}개의 코인을 받았습니다.")
            return reward
        else:
            print(f"{self.name}는 이미 DAO 티켓을 태웠거나, 태울 티켓이 없습니다.")
            return 0

    def final_coins(self):
        # DAO 티켓이 남아 있으면 평판 점수 * 10, 없으면 평판 점수 * 5
        if self.dao_tickets > 0:
            return self.reputation * 10
        else:
            return self.reputation * 5

def show_status(player, team_bank, teams, team_banks):
    print(f"\n--- {player.name}의 현재 상태 ---")
    print(f"팀 은행: {team_bank} 코인")
    print(f"평판 점수: {player.reputation}")
    print(f"현재 코인: {player.coins}")
    print(f"DAO 티켓: {player.dao_tickets}")
    
    # 팀 내 랭킹
    team_ranking = sorted(teams[player.team_id], key=lambda p: p.coins + (p.reputation * 10), reverse=True)
    user_rank = team_ranking.index(player) + 1
    print(f"팀 내 랭킹: {user_rank}위 / {len(team_ranking)}명")
    
    # 전체 팀 랭킹
    overall_team_ranking = sorted(team_banks.items(), key=lambda x: x[1], reverse=True)
    print("\n--- 전체 팀 랭킹 ---")
    for rank, (team_id, bank) in enumerate(overall_team_ranking, start=1):
        print(f"{rank}위: 팀 {team_id}, 은행 코인: {bank:.2f}")

def show_commands():
    print("\n--- 명령어 목록 ---")
    print("coin: 코인 10개를 받습니다.")
    print("bank: 팀 은행에 1~5개의 코인을 추가합니다.")
    print("vote: 도박 투표를 진행합니다.")
    print("burn: DAO 티켓을 태워 보상을 받습니다.")
    print("status: 현재 상태를 확인합니다.")
    print("commands: 명령어 목록을 확인합니다.")

def play_game():
    # 각 팀당 플레이어 생성
    teams = {team_id: [Player(f"Player {i} (Team {team_id})", team_id) for i in range(1, TEAM_SIZE + 1)] 
             for team_id in range(1, TOTAL_TEAMS + 1)}

    user_team_id = random.choice(list(teams.keys()))
     # 유저 이름을 입력받고, 유저를 생성
    user_name = input("당신의 이름을 입력하세요: ")
    user = Player(user_name, user_team_id, is_user=True)
    teams[user_team_id][0] = user  # 유저는 첫 번째 플레이어로 설정
   
    team_banks = {team_id: 0 for team_id in range(1, TOTAL_TEAMS + 1)}  # 각 팀의 팀 은행
    rounds = 10

    for turn in range(1, rounds + 1):
        print(f"\n=== Turn {turn} ===")
        for team_id, players in teams.items():
            total_dao_tickets = sum([p.dao_tickets for p in players])  # 현재 팀 내 남은 DAO 티켓 수 계산
            for player in players:
                # 매 턴 유저는 선택을 할 수 있음
                if player.is_user:
                    while True:
                        action = input(f"{player.name}, 행동을 선택하세요 (coin/bank/status/commands): ").strip().lower()
                        if action == "coin":
                            player.receive_coins()
                            print(f"{player.name}가 코인 10개를 받았습니다.")
                            break
                        elif action == "bank":
                            contribution = player.add_to_bank()
                            team_banks[team_id] += contribution
                            print(f"외부에서 팀 {team_id} 은행에 {contribution}개의 코인이 추가되었습니다.")
                            break
                        elif action == "status":
                            show_status(player, team_banks[team_id], teams, team_banks)
                        elif action == "commands":
                            show_commands()
                        else:
                            print("잘못된 명령어입니다. 다시 입력해주세요.")
                else:
                    # 다른 플레이어는 랜덤하게 행동
                    action = random.choice(["coin", "bank"])
                    if action == "coin":
                        player.receive_coins()
                        print(f"{player.name}가 코인 10개를 받았습니다.")
                    else:
                        contribution = player.add_to_bank()
                        team_banks[team_id] += contribution
                        print(f"외부에서 팀 {team_id} 은행에 {contribution}개의 코인이 추가되었습니다.")

            # 유저 도박 투표
            print("\n=== 도박 투표 ===")
            vote_yes = 0
            vote_no = 0
            for player in teams[team_id]:
                votes = player.vote_power()
                if player.is_user:
                    while True:
                        vote = input(f"{player.name}, 도박에 참여하시겠습니까? (yes/no): ").strip().lower()
                        if vote == "yes":
                            vote_yes += votes
                            break
                        elif vote == "no":
                            vote_no += votes
                            break
                        else:
                            print("잘못된 입력입니다. yes 또는 no로 입력하세요.")
                    print(f"현재 평판 점수: {player.reputation}, 투표권: {votes}개")
                else:
                    # 다른 플레이어는 랜덤으로 투표
                    if random.choice([True, False]):
                        vote_yes += votes
                    else:
                        vote_no += votes

            if vote_yes > vote_no:
                if random.choice([True, False]):
                    print(f"팀 {team_id} 도박 성공! 팀 은행의 20%가 증가합니다.")
                    team_banks[team_id] *= 1.2
                else:
                    print(f"팀 {team_id} 도박 실패! 팀 은행의 20%가 감소합니다.")
                    team_banks[team_id] *= 0.8
            print(f"현재 팀 은행: {team_banks[team_id]:.2f} 코인")

            # DAO 티켓 태우기 여부
            if team_id == user_team_id:
                while True:
                    burn = input("DAO 티켓을 태우시겠습니까? (yes/no): ").strip().lower()
                    if burn == "yes":
                        user.burn_ticket(team_banks[team_id], total_dao_tickets)
                        break
                    elif burn == "no":
                        print("DAO 티켓을 태우지 않았습니다.")
                        break
                    else:
                        print("잘못된 입력입니다. yes 또는 no로 입력하세요.")
    
    # 최종 계산 및 결과
    print("\n=== 게임 종료 ===")
    winning_team = max(team_banks, key=team_banks.get)
    print(f"\n우승팀은 팀 {winning_team}입니다!")
    
    for team_id, players in teams.items():
        print(f"\n--- 팀 {team_id} 결과 ---")
        for player in players:
            final_coins = player.final_coins()
            print(f"{player.name}: 최종 코인 {final_coins}개, 평판: {player.reputation}")

    # 개인 우승 확인
    if user_team_id == winning_team:
        print("\n축하합니다! 당신은 우승팀에 속해 있습니다!")
    else:
        # 팀 내에서 1위 확인
        user_final_coins = user.final_coins()
        team_top_player = max(teams[user_team_id], key=lambda p: p.final_coins())
        if team_top_player == user:
            print("\n축하합니다! 당신은 팀 내에서 1위를 차지했습니다!")
        else:
            print("\n안타깝게도 당신은 팀에서 1위를 차지하지 못했습니다.")

if __name__ == "__main__":
    play_game()
