import sys
import random

class MDP:
    """Markov Decision Process class"""
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
        self.init_states()

    def init_states(self):
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
    def get_state(self,coords):
        """Returns the state given the coordinates"""
        for state in self.states:
            if state.coords == coords:
                return state
        return Exception("State not found.")
    def get_next_state(self, state, action):
        """Returns the next state given the current state and action"""
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
    
    def print_grid(self, policy = None, Q = None):
        """Prints the grid with the states. Used for debugging."""
        if Q is not None:
            for j in range(1,self.N+1)[::-1]:
                for i in range(1,self.M+1):
                    state = self.get_state((i,j))
                    if state.type == "D":
                        print(max(self.actions, key=lambda x: Q[state][x]), end=" ")
                    else:
                        print(state.type, end=" ")
                print()
            return
        if policy is not None:
            for j in range(1,self.N+1)[::-1]:
                for i in range(1,self.M+1):
                    state = self.get_state((i,j))
                    if state.type == "D":
                        print(policy[state], end=" ")
                    else:
                        print(state.type, end=" ")
                print()
            return
        for j in range(1,self.N+1)[::-1]:
            for i in range(1,self.M+1):
                state = self.get_state((i,j))
                if state.type == "D":
                    print("_", end=" ")
                else:
                    print(state.type, end=" ")
            print()
        
class State:
    """State class"""
    def __init__(self, coords, state_type, reward):
        self.coords = coords
        self.type = state_type
        self.reward = reward

def parse_input(input_file):
    """Parses the input file and returns the parameters"""
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
    V = {} # Value function

    #initialize the value function
    for state in mdp.states:
            V[state] = 0

    while True:
        delta = 0
        for state in mdp.states:
            # Skip pitfall and goal states
            if state.type != "D":
                continue

            v = V[state]
            action = policy[state]
            next_state = mdp.get_next_state(state, action)
            V[state] = next_state.reward + gamma * V[next_state]
            delta = max(delta, abs(v - V[state]))
        if delta < theta:
            break
    return V

def policy_improvement(mdp, V, gamma):
    policy = {}
    for state in mdp.states:
        max_val = float('-inf')
        best_action = None
        for action in mdp.actions:
            next_state = mdp.get_next_state(state, action)
            val = next_state.reward + gamma * V[next_state]
            if val > max_val:
                max_val = val
                best_action = action
        policy[state] = best_action # Update the policy
    return policy

def policy_iteration(parsed_input):
    theta, gamma, M, N, num_obstacles, obstacle_coords, num_pitfalls,pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal = parsed_input[1:]
    # Initialize the MDP
    mdp = MDP(M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal)
    # Initialize the policy
    policy = {}
    # Initialize the value function
    V = {}
    for state in mdp.states:
        policy[state] = 0

    while True:
        V = policy_evaluation(mdp, policy, gamma, theta)
        new_policy = policy_improvement(mdp, V, gamma)
        if new_policy == policy:
            break
        policy = new_policy
    result = ""
    #traverse the policy
    for state in mdp.states:
        result += f"{state.coords[0]} {state.coords[1]} {policy[state]}\n"
    
    return result

def choose_action(Q, state, epsilon):
    """Choose an action based on epsilon-greedy policy"""
    if random.uniform(0, 1) < epsilon:
        return random.choice(list(Q[state].keys()))
    return max(Q[state], key=Q[state].get) 


def sarsa(parsed_input):
    num_episodes, alpha, gamma, epsilon, M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal = parsed_input[1:]
    # Initialize the MDP
    mdp = MDP(M, N, num_obstacles, obstacle_coords, num_pitfalls, pitfall_coords, goal_state, r_def, r_obs, r_pit, r_goal)

    # Initialize Q
    Q = {state: {action: 0 for action in mdp.actions} for state in mdp.states}
    default_states = [state for state in mdp.states if state.type == "D"]
    
    for _ in range(num_episodes):
        state = random.choice(default_states)
        action = choose_action(Q, state, epsilon)
        
        while state.type != "G": # Continue until goal state is reached
            next_state = mdp.get_next_state(state, action)
            
            if next_state.type == "O":
                # Penalize and skip updating state
                Q[state][action] = Q[state][action] + alpha * (r_obs + gamma * Q[state][action] - Q[state][action])
                action = choose_action(Q, state, epsilon)
                continue
            
            next_action = choose_action(Q, next_state, epsilon)
            
            # Update Q-value
            Q[state][action] += alpha * (next_state.reward + gamma * Q[next_state][next_action] - Q[state][action])
            
            if next_state.type == "P":
                break  # End the episode if a pitfall is encountered
            
            # Move to the next state and action
            state = next_state
            action = next_action
    
    # Generate result
    result = ""
    for state in mdp.states:
        best_action = max(mdp.actions, key=lambda x: Q[state][x])
        result += f"{state.coords[0]} {state.coords[1]} {best_action}\n"
    
    return result



def main():
    #Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Parse the input file
    parsed_input = parse_input(input_file)
    method = parsed_input[0]
    if method == "P":
        #Write to output file
        with open(output_file, 'w') as outfile:
            outfile.write(policy_iteration(parsed_input))
    elif method == "S":
        with open(output_file, 'w') as outfile:
            outfile.write(sarsa(parsed_input))
    else:
        print("Error: Invalid method.")
        sys.exit(1)


if __name__ == "__main__":
    main()
