import sys
import collections
import random

class MDP:
    def __init__(self, M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal):
        self.M = M
        self.N = N
        self.num_obstacles = num_obstacles
        self.obstacle_coords = obstacle_coords
        self.num_pitfalls = num_pitfalls
        self.pitfall_coords = pitfall_coords
        self.goal_state = goal_state
        self.r_def = r_def
        self.r_obs = r_obs
        self.r_pit = r_pit
        self.r_goal = r_goal
        self.states = []
        self.actions = [0,1,2,3] # 0: Up, 1: Right, 2: Down, 3: Left
        self.transitions = {}
        #self.rewards = {}
        self.initialize_states()
        #self.initialize_rewards()

    def initialize_states(self):
        for i in range(1,self.M+1):
            for j in range(1,self.N+1):
                if (i,j) == self.goal_state:
                    self.states.append(State((i,j), "G", self.r_goal))
                elif (i,j) in self.obstacle_coords:
                    self.states.append(State((i,j), "O", self.r_obs))
                elif (i,j) in self.pitfall_coords:
                    self.states.append(State((i,j), "P", self.r_pit))
                else:
                    self.states.append(State((i,j), "D", self.r_def))
    # def initialize_rewards(self):
    #     for state in self.states:
    #         self.rewards[state] = {}
    #         for action in self.actions:
    #             self.rewards[state][action] = {}
    #             if action == 0: # Up     
    #                 if state.coords[1] == self.M:
    #                     self.rewards[state][action] = self.r_obs # treat out of bounds as obstacle
    #                 else:
    #                     self.rewards[state][action] = self.get_state((state.coords[0], state.coords[1]+1)).reward
    #             elif action == 2: # Down
    #                 if state.coords[1] == 1:
    #                     self.rewards[state][action] = self.r_obs # treat out of bounds as obstacle
    #                 else:
    #                     self.rewards[state][action] = self.get_state((state.coords[0], state.coords[1]-1)).reward
    #             elif action == 3: # Left
    #                 if state.coords[0] == 1:
    #                     self.rewards[state][action] = self.r_obs # treat out of bounds as obstacle
    #                 else:
    #                     self.rewards[state][action] = self.get_state((state.coords[0]-1, state.coords[1])).reward
    #             elif action == 1: # Right
    #                 if state.coords[0] == self.N:
    #                     self.rewards[state][action] = self.r_obs # treat out of bounds as obstacle
    #                 else:
    #                     self.rewards[state][action] = self.get_state((state.coords[0]+1, state.coords[1])).reward
    def get_state(self,coords):
        for state in self.states:
            if state.coords == coords:
                return state
        return Exception("State not found.")
    def get_next_state(self, state, action):
        if action == 0:
            if state.coords[1] == self.M:
                return state
            return self.get_state((state.coords[0], state.coords[1]+1))
        if action == 2:
            if state.coords[1] == 1:
                return state
            return self.get_state((state.coords[0], state.coords[1]-1))
        if action == 3:
            if state.coords[0] == 1:
                return state
            return self.get_state((state.coords[0]-1, state.coords[1]))
        if action == 1:
            if state.coords[0] == self.N:
                return state
            return self.get_state((state.coords[0]+1, state.coords[1]))
        return Exception("Invalid action.")
    def print_grid(self):
        for j in range(1,self.N+1)[::-1]:
            for i in range(1,self.M+1):
                state = self.get_state((i,j))
                print(f"{state.type} ", end=" ")
            print()
        
class State:
    def __init__(self, coords, type, reward):
        self.coords = coords
        self.type = type
        self.reward = reward

def parse_input(input_file):
    try:
        with open(input_file, 'r') as infile:
            data = infile.read()
            data = data.splitlines()
            method = data[0]
            if method == "P":
                theta = float(data[1])
                gamma = float(data[2])
                M,N = map(int, data[3].split()[::-1])
                num_obstacles = int(data[4])
                obstacle_coords = []
                for i in range(num_obstacles):
                    obstacle_coords.append(tuple(map(int, data[5+i].split())))
                num_pitfalls = int(data[5+num_obstacles])
                pitfall_coords = []
                for i in range(num_pitfalls):
                    pitfall_coords.append(tuple(map(int, data[6+num_obstacles+i].split())))
                goal_state = tuple(map(int, data[6+num_obstacles+num_pitfalls].split()))
                r_def, r_obs, r_pit, r_goal = map(float, data[7+num_obstacles+num_pitfalls].split())
                # print(f"Method: {method}")
                # print(f"Theta: {theta}")
                # print(f"Gamma: {gamma}")
                # print(f"M: {M}")
                # print(f"N: {N}")
                # print(f"Number of obstacles: {num_obstacles}")
                # print(f"Obstacle coordinates: {obstacle_coords}")
                # print(f"Number of pitfalls: {num_pitfalls}")
                # print(f"Pitfall coordinates: {pitfall_coords}")
                # print(f"Goal state: {goal_state}")
                # print(f"Reward for default state: {r_def}")
                # print(f"Reward for obstacle state: {r_obs}")
                # print(f"Reward for pitfall state: {r_pit}")
                # print(f"Reward for goal state: {r_goal}")
                return method, theta, gamma, M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal
            if method == "S":
                num_episodes = int(data[1])
                alpha = float(data[2])
                gamma = float(data[3])
                epsilon = float(data[4])
                M,N = map(int, data[5].split())
                num_obstacles = int(data[6])
                obstacle_coords = []
                for i in range(num_obstacles):
                    obstacle_coords.append(tuple(map(int, data[7+i].split())))
                num_pitfalls = int(data[7+num_obstacles])
                pitfall_coords = []
                for i in range(num_pitfalls):
                    pitfall_coords.append(tuple(map(int, data[8+num_obstacles+i].split())))
                goal_state = tuple(map(int, data[8+num_obstacles+num_pitfalls].split()))
                r_def, r_obs, r_pit, r_goal = map(float, data[9+num_obstacles+num_pitfalls].split())
                # print(f"Method: {method}")
                # print(f"Number of episodes: {num_episodes}")
                # print(f"Alpha: {alpha}")
                # print(f"Gamma: {gamma}")
                # print(f"Epsilon: {epsilon}")
                # print(f"M: {M}")
                # print(f"N: {N}")
                # print(f"Number of obstacles: {num_obstacles}")
                # print(f"Obstacle coordinates: {obstacle_coords}")
                # print(f"Number of pitfalls: {num_pitfalls}")
                # print(f"Pitfall coordinates: {pitfall_coords}")
                # print(f"Goal state: {goal_state}")
                # print(f"Reward for default state: {r_def}")
                # print(f"Reward for obstacle state: {r_obs}")
                # print(f"Reward for pitfall state: {r_pit}")
                # print(f"Reward for goal state: {r_goal}")
                return method, num_episodes, alpha, gamma, epsilon, M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal
            print("Error: Invalid method.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def policy_evaluation(mdp,policy, gamma, theta):
    V = {}
    for state in mdp.states:
            V[state] = state.reward
    while True:
        delta = 0
        for state in mdp.states:
            if state.type != "D":
                continue
            v = V[state]
            action = policy[state]
            next_state = mdp.get_next_state(state, action)
            V[state] = next_state.reward + gamma * V[next_state]
            delta = max(delta, abs(v - V[state])) # Not sure if this is correct
        if delta < theta:
            break
    return V

def policy_improvement(mdp, V, gamma):
    policy = {}
    for state in mdp.states:
        max_val = float('-inf')
        best_action = 0
        for action in mdp.actions:
            next_state = mdp.get_next_state(state, action)
            val = next_state.reward + gamma * V[next_state]
            if val > max_val:
                max_val = val
                best_action = action
        policy[state] = best_action
    return policy

def policy_iteration(parsed_input):
    theta, gamma, M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal = parsed_input[1:]
    # Initialize the MDP
    mdp = MDP(M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal)
    mdp.print_grid()
    # Initialize the policy
    policy = {}
    policy_changed = True
    # Initialize the value function
    V = {}
    for state in mdp.states:
        policy[state] = 0

    while policy_changed:
        policy_changed = False
        V = policy_evaluation(mdp, policy, gamma, theta)
        new_policy = policy_improvement(mdp, V, gamma)
        if new_policy != policy:
            policy_changed = True
            policy = new_policy
    result = ""
    #traverse the policy
    for state in mdp.states:
        result += f"{state.coords[0]} {state.coords[1]} {policy[state]}\n"
    return result

def sarsa(parsed_input):
    NotImplementedError("SARSA is not implemented yet.")

def main():
    # Check if the correct number of arguments is provided
    # if len(sys.argv) != 2:
    #     sys.exit(1)
    input_file = ".\\sample_io\\input_p_1.txt"
    output_file = ".\\sample_io\\output_p_1.txt"

    # Parse the input file
    parsed_input = parse_input(input_file)
    method = parsed_input[0]
    if method == "P":
        #Write to output file
        with open(output_file, 'w') as outfile:
            outfile.write(policy_iteration(parsed_input))


    else:
        with open(output_file, 'w') as outfile:
            outfile.write(sarsa(parsed_input))


if __name__ == "__main__":
    main()
