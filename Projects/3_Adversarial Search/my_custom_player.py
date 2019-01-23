
from sample_players import DataPlayer
from isolation.isolation import DebugState 
from heapdict import heapdict
import random,math

HASH_SIZE = 1000

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    
    EXPAND_TIMEOUT = 10         

    def manhattan_dist(self, pointa, pointb):
        return abs(pointa[0] - pointb[0]) + abs(pointa[1] - pointb[1])

    def euclidean(self, pointa, pointb):
        return math.sqrt((pointa[0] - pointb[0])**2 + (pointa[1] - pointb[1])**2)    

    def zero_sum_h(self, state):
        """
            - This heuristic is default heuristic introduced by mentors.
            
            - Idea : if current player has more available actions greater than 
                     opponent this acquire that this state is good
            
            - Equation : current player available moves - opponent player available moves

            - Analysis : 50% against self 54.0% against minimax 74.2% against GREEDY 95.2% against Random             
        """
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        if(own_liberties == 0):
            return float("-inf")
        elif(opp_liberties == 0):
            return float("inf")

        return len(own_liberties) - 3 * len(opp_liberties) 

    def keep_near_center_h(self, state):
        """
            - This heuristic follows "keep your enemies closer" .
            
            - Idea : player will choose action that make him near to obstacle
            
            - Equation : manhattan distances from enemy player

            - Analysis : 50% against self 47.2% against minimax 76.5% against GREEDY 94.0% against Random                         
        """
        def cal(matrix):
            total = 0 
            px = 0
            py = 0
            ex = 0 
            ey = 0
            cx = int(len(matrix)/2)
            cy = int(len(matrix[0])/2)
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == -1:
                        px = i
                        py = j
                    if matrix[i][j] == 2:
                        ex = i
                        ey = j    
            return - self.manhattan_dist((px,py), (cx,cy))                         
  

        x = self.zero_sum_h(state)
        if x == 0:
            return cal(state.obstacles_matrix()) / state.ply_count   
        return x

    def keep_near_center_h2(self, state):
        """
            - This heuristic follows "keep your enemies closer" .

            - Idea : player will choose action that make him near to obstacle

            - Equation : manhattan distances from enemy player

            - Analysis : 50% against self 47.2% against minimax 76.5% against GREEDY 94.0% against Random                         
        """
        def cal_2(matrix):

            own_loc = state.locs[self.player_id]
            opp_loc = state.locs[1 - self.player_id]
            own_liberties = state.liberties(own_loc)
            opp_liberties = state.liberties(opp_loc)

            x = 0

            if(own_liberties == 0):
                x = float("-inf")
            elif(opp_liberties == 0):
                x = float("inf")
            else:
                x = len(own_liberties) - 3 * len(opp_liberties) 

            px = 0
            py = 0
            ex = 0 
            ey = 0
            cx = int(len(matrix)/2)
            cy = int(len(matrix[0])/2)
            
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == -1:
                        px = i
                        py = j
                    if matrix[i][j] == 2:
                        ex = i
                        ey = j
            
            obstacles = 0                
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 1 and abs(i-px) <= 2 and abs(j-py) <= 2:
                        obstacles += 1    

            near_center = -self.manhattan_dist((px,py) , (cx,cy)) / (math.sqrt(state.ply_count))
            away_from_obstacles = -obstacles / 25 
            # print(zero_sum,near_center,away_from_obstacles)
            #print("near_center = ", near_center, " away_from_obstacles = ",away_from_obstacles ,"zero_sum = ", x)
            if x == 0 and math.fabs(away_from_obstacles) <= 0.25 :
                return near_center
            elif x == 0 and math.fabs(away_from_obstacles) > 0.75:
                 return away_from_obstacles
            return x                           

            
        res = cal_2(state.obstacles_matrix())    
        #print(res)

        return res   

    def keep_near_center_h_3(self, state):
        """
            - This heuristic follows "keep your enemies closer" .
            
            - Idea : player will choose action that make him near to obstacle
            
            - Equation : manhattan distances from enemy player

            - Analysis : 50% against self 56.2% against minimax 78.5% against GREEDY 95.0% against Random                         
        """
        def cal(matrix):
            total = 0 
            px = 0
            py = 0
            ex = 0 
            ey = 0
            cx = int(len(matrix)/2)
            cy = int(len(matrix[0])/2)
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == -1:
                        px = i
                        py = j
                    if matrix[i][j] == 2:
                        ex = i
                        ey = j
            obstacles = 0                
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 1 and abs(i-px) <= 2 and abs(j-py) <= 2:
                        obstacles += 1    

            return -self.manhattan_dist((px,py) , (cx,cy)) / state.ply_count , obstacles / 25 , -self.manhattan_dist((px,py) , (ex,ey))                         

        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)    

        x = self.zero_sum_h(state)
        y,z,l = cal(state.obstacles_matrix()) 
        if x != 0:
            return x
        elif abs(y) >= 1:
            return y
        elif z != 0:        
            return z
        else:
            return l
                      
    def get_action(self, state):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 3 plies
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax(state, depth=3, heuristic=self.keep_near_center_h2))       

    def minimax(self, state, depth, heuristic):

        mem = heapdict()

        def min_value(state, depth, alpha, beta):
            mem_state = (state.board,state.locs[0],state.locs[1],state.player())
            if mem_state in mem:
                return mem[mem_state]
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return heuristic(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            mem[mem_state] = value                 
            return value

        def max_value(state, depth, alpha, beta):
            mem_state = (state.board,state.locs[0],state.locs[1],state.player())
            if mem_state in mem:
                return mem[mem_state]
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return heuristic(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            mem[mem_state] = value        
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1, float("-inf"), float("inf")))

