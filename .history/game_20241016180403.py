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
        self.coins = STARTING_COINS
        self.reputation = 0
        self.dao_tickets = 1
        self.is_user = is_user

    def contribute(self):
        contribution = random.randint(1, TEAM_SIZE)
        self.reputation += random.randint(1, 5)
        self.coins -= contribution
        return contribution

    def keep(self):
        self.coins += 1

    def vote_power(self):
        return round(math.sqrt(self.reputation))

    def burn_ticket(self, team_bank):
        reward = team_bank / TEAM_SIZE / 2
        self.coins += reward
        return reward

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
        # 각 팀의 플레이어 행동 처리
        for team_id, players in teams.items():
            for player in players:
                if player.is_user:
                    action = input(f"{player.name}, 행동을 선택하세요 (contribute/keep): ").strip().lower()
                else:
                    action = random.choice(["contribute", "keep"])

                if action == "contribute":
                    contribution = player.contribute()
                    team_banks[team_id] += contribution
                    print(f"{player.name}가 {contribution}개의 코인을 팀 은행에 기부했습니다.")
                elif action == "keep":
                    player.keep()
                    print(f"{player.name}가 코인 1개를 킵했습니다.")
        
        # 각 팀별 도박 투표
        for team_id, players in teams.items():
            print(f"\n=== 팀 {team_id}의 도박 투표 ===")
            vote_yes = 0
            vote_no = 0
            for player in players:
                votes = player.vote_power()
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
            print(f"팀 {team_id}의 현재 팀 은행: {team_banks[team_id]:.2f} 코인")
    
    # 최종 계산 및 결과
    print("\n=== 게임 종료 ===")
    winning_team = max(team_banks, key=team_banks.get)
    print(f"\n우승팀은 팀 {winning_team}입니다!")
    
    for team_id, players in teams.items():
        print(f"\n--- 팀 {team_id} 결과 ---")
        for player in players:
            final_coins = player.coins + (player.reputation // 2)
            print(f"{player.name}: {final_coins} 코인, 평판: {player.reputation}")

    # 개인 우승 확인
    if user_team_id == winning_team:
        print("\n축하합니다! 당신은 우승팀에 속해 있습니다!")
    else:
        # 팀 내에서 1위 확인
        user_final_coins = user.coins + (user.reputation // 2)
        team_top_player = max(teams[user_team_id], key=lambda p: p.coins + (p.reputation // 2))
        if team_top_player == user:
            print("\n축하합니다! 당신은 팀 내에서 1위를 차지했습니다!")
        else:
            print("\n안타깝게도 당신은 팀에서 1위를 차지하지 못했습니다.")

if __name__ == "__main__":
    play_game()
