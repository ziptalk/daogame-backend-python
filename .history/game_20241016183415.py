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
        self.coins = 0  # 매 턴마다 10개의 코인이 지급되므로 초기 코인은 0
        self.reputation = 0
        self.dao_tickets = 1
        self.is_user = is_user
        self.burned_tickets = False

    def receive_coins(self):
        # 매 턴마다 플레이어는 10개의 코인을 받습니다.
        self.coins = 10

    def contribute(self):
        # 팀 은행에 자신이 가진 모든 코인을 기부
        contribution = self.coins
        self.coins = 0
        self.reputation += random.randint(1, 5)  # 기여 시 평판 점수 증가
        return contribution

    def vote_power(self):
        return round(math.sqrt(self.reputation))

    def final_coins(self):
        # 평판 점수 * 10 코인으로 보상
        return self.reputation * 10

    def burn_ticket(self, team_bank):
        if not self.burned_tickets:
            reward = team_bank / TEAM_SIZE / 2
            self.coins += reward
            self.burned_tickets = True
            print(f"{self.name}가 DAO 티켓을 태워 {reward:.2f}개의 코인을 받았습니다.")
            return reward
        else:
            print(f"{self.name}는 이미 DAO 티켓을 태웠습니다.")
            return 0

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
    print("contribute: 코인을 팀 은행에 기부합니다.")
    print("keep: 코인을 킵합니다.")
    print("vote: 도박 투표를 진행합니다.")
    print("burn: DAO 티켓을 태워 보상을 받습니다.")
    print("status: 현재 상태를 확인합니다.")
    print("commands: 명령어 목록을 확인합니다.")

def play_game():
    # 각 팀당 플레이어 생성
    teams = {team_id: [Player(f"Player {i} (Team {team_id})", team_id) for i in range(1, TEAM_SIZE + 1)] 
             for team_id in range(1, TOTAL_TEAMS + 1)}

    user_team_id = random.choice(list(teams.keys()))
    user = Player("User", user_team_id, is_user=True)
    teams[user_team_id][0] = user  # 유저는 첫 번째 플레이어로 설정

    team_banks = {team_id: 0 for team_id in range(1, TOTAL_TEAMS + 1)}  # 각 팀의 팀 은행
    rounds = 10

    for turn in range(1, rounds + 1):
        print(f"\n=== Turn {turn} ===")
        for team_id, players in teams.items():
            # 각 턴마다 팀이 외부로부터 랜덤 코인 받거나, 각 플레이어가 10개씩 코인 받음
            external_fund = random.choice([True, False])  # 외부 자금 여부 결정
            if external_fund:
                # 외부에서 팀 은행에 10~50개의 코인 주어짐
                team_contribution = random.randint(10, 50)
                team_banks[team_id] += team_contribution
                print(f"팀 {team_id}는 외부로부터 {team_contribution}개의 코인을 받았습니다.")
            else:
                # 각 플레이어가 10개의 코인을 받음
                for player in players:
                    player.receive_coins()
                    if player.is_user:
                        while True:
                            action = input(f"{player.name}, 행동을 선택하세요 (contribute/keep/status/commands): ").strip().lower()
                            if action == "contribute":
                                contribution = player.contribute()
                                team_banks[team_id] += contribution
                                print(f"{player.name}가 {contribution}개의 코인을 팀 은행에 기부했습니다.")
                                break
                            elif action == "keep":
                                print(f"{player.name}가 코인 10개를 킵했습니다.")
                                break
                            elif action == "status":
                                show_status(player, team_banks[team_id], teams, team_banks)
                            elif action == "commands":
                                show_commands()
                            else:
                                print("잘못된 명령어입니다. 다시 입력해주세요.")
                    else:
                        action = random.choice(["contribute", "keep"])
                        if action == "contribute":
                            contribution = player.contribute()
                            team_banks[team_id] += contribution
                            print(f"{player.name}가 {contribution}개의 코인을 팀 은행에 기부했습니다.")
                        else:
                            print(f"{player.name}가 코인 10개를 킵했습니다.")
        
        # 유저 도박 투표
        print("\n=== 도박 투표 ===")
        vote_yes = 0
        vote_no = 0
        for player in teams[user_team_id]:
            if player.is_user:
                while True:
                    vote = input(f"{player.name}, 도박에 참여하시겠습니까? (yes/no): ").strip().lower()
                    if vote == "yes":
                        vote_yes += player.vote_power()
                        break
                    elif vote == "no":
                        vote_no += player.vote_power()
                        break
                    else:
                        print("잘못된 입력입니다. yes 또는 no로 입력하세요.")
            else:
                if random.choice([True, False]):
                    vote_yes += player.vote_power()
                else:
                    vote_no += player.vote_power()

        if vote_yes > vote_no:
            if random.choice([True, False]):
                print(f"팀 {user_team_id} 도박 성공! 팀 은행의 20%가 증가합니다.")
                team_banks[user_team_id] *= 1.2
            else:
                print(f"팀 {user_team_id} 도박 실패! 팀 은행의 20%가 감소합니다.")
                team_banks[user_team_id] *= 0.8
        print(f"현재 팀 은행: {team_banks[user_team_id]:.2f} 코인")

        # DAO 티켓 태우기 여부
        while True:
            burn = input("DAO 티켓을 태우시겠습니까? (yes/no): ").strip().lower()
            if burn == "yes":
                user.burn_ticket(team_banks[user_team_id])
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

