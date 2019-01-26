
from sample_players import DataPlayer
from isolation.isolation import DebugState
import random,math,time


class Heuristics:


    def __init__(self, player_id):
        self.player_id = player_id

    def obstacles_matrix(self,state): 
        """
           transform board encoding int 2-d matrix to determine positions of obstalces 
        """    
        _WIDTH = 11
        _HEIGHT = 9
        _SIZE = (_WIDTH + 2) * _HEIGHT - 2

        arr = [[] for i in range(_WIDTH - 2)]
        i = 0
        board = state.board << 2
        for loc in range(_SIZE + 2):
            if loc > 2 and loc % (_WIDTH + 2) == 0:
                i+=1
            if loc % (_WIDTH + 2) == 0 or loc % (_WIDTH + 2) == 1:
                continue
            sym = int((board & (1 << loc)) == 0)
            if loc-2 == state.locs[1 - state.player()]: sym = 2
            if loc-2 == state.locs[state.player()]: sym = -1
            arr[i].append(sym)
        
        arr.reverse()         
        for a in arr:
            a.reverse()
        return arr       


    def manhattan_dist(self, pointa, pointb):
        """
            calulate manhttan distance between two points in 2-d plane
        """
        return abs(pointa[0] - pointb[0]) + abs(pointa[1] - pointb[1])

    def euclidean(self, pointa, pointb):
        """
            calulate euclidean distance between two points in 2-d plane
        """
        return math.sqrt((pointa[0] - pointb[0])**2 + (pointa[1] - pointb[1])**2)    

    def default_h(self, state):
        """
            - This heuristic is modification on default heuristic introduced by mentors.
            
            - Idea : if current player has more available actions greater than 
                     opponent this acquire that this state is good
            
            - Equation : current player available moves - 3 * opponent player available moves

            - Analysis : 50% against self 70% against minimax 86.2% against GREEDY 95.2% against Random             
        """
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        if(own_liberties == 0):
            return float("-inf")
        elif(opp_liberties == 0):
            return float("inf")

        return len(own_liberties) - len(opp_liberties) 
    

    def zero_sum_h(self, state):
        """
            - This heuristic is modification on default heuristic introduced by mentors.
            
            - Idea : if current player has more available actions greater than 
                     opponent this acquire that this state is good
            
            - Equation : current player available moves - 3 * opponent player available moves

            - Analysis : 50% against self 70% against minimax 86.2% against GREEDY 95.2% against Random             
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
            - This heuristic favourites states at center of grid as it has highly positional state at begging of game.
            
            - Idea : player will choose action that make him near to center if zero_sum heuristic is zero 
            
            - Equation : - manhattan distances of player from center

            - Analysis : 50% against self 79.8% against minimax 89.5% against GREEDY 97.8% against Random                         
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
            return -self.manhattan_dist((px,py), (cx,cy))                         
  

        x = self.zero_sum_h(state)
        if x == 0:
            return cal(self.obstacles_matrix(state)) / state.ply_count   
        return x

    def keep_near_center_h2(self, state):
        """
            - This heuristic is modification of keep_near_center_h where not always going towards center is good when 
              there's alot of obstacles in this state, so when percentage of obstacles in 5*5 box around player has 
              more than 25% obstacles, this heuristic return negative percentage of obstales.

            - Idea : player will choose action that make him near to obstacle

            - Equation : -percentage of obstacles in 5*5 matrices

            - Analysis : 50% against self 65.2% against minimax 86.0% against GREEDY 96.5% against Random                         
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

            if x == 0 and math.fabs(away_from_obstacles) <= 0.25 :
                return near_center
            elif x == 0 and math.fabs(away_from_obstacles) > 0.75:
                 return away_from_obstacles
            return x                           

            
        res = cal_2(self.obstacles_matrix(state))

        return res   

    def keep_near_center_h3(self, state):
        """
            - This heuristic modifies keep_near_center_h2 where in some cases at end of game where effect of near_center heuristic decreases,
              this heuristic favourites to go near opponent.
            
            - Idea : player will choose action that make him near enemy if zero_sum heuristic and near_center effect is small and there's
                     small obstacles around.  
            
            - Equation : manhattan distances from enemy player

            - Analysis : 50% against self 75.0% against minimax 90.5% against GREEDY 97.0% against Random                         
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

        x = self.zero_sum_h(state)
        y,z,l = cal(self.obstacles_matrix(state)) 

        if x != 0:
            return x
        elif abs(y) >= 1:
            return y
        elif z != 0:        
            return z
        else:
            return l

class CustomPlayer(DataPlayer):

    """
        Game agent that uses minmax with alpha-beta algorithm in addition to memorizing 
        states values to find best action in specific time which is less than a second.
    """

    
    # max time in expanding search tree
    EXPAND_TIMEOUT = 0.1    

                              
    def get_action(self, state):
        """ 
            Choose an action available in the current state
        """
        
        # start expansions time 
        self.start = time.time()

        # initialize heuristic
        H = Heuristics(self.player_id)
        
        # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 10 plies
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax_ab_mem(state, depth=10, heuristic = H.keep_near_center_h))       

    # memorization of value of states given state : (board, player1_place, player2_place, turns)          
    mem = {}        

    def minimax_ab_mem(self, state, depth, heuristic):

        """
            Game-playing agent that chooses a move using your evaluation function
            and a depth-limited minimax algorithm with alpha-beta pruning, agent expand 
            nodes when time is below expansion time which is 0.1 sec.
            
            Parameters
            ----------

            - heuristic : used to calculate value od state based on certain heuristic

            - state : current state that of the game

            - depth : max depth of search tree 

        """

        def min_value(state, depth, alpha, beta):

            # memorization state used as a key 
            mem_state = (state.board,state.locs[0],state.locs[1],state.player())
            
            #-------------------------------------------------------------------#
            #  stop expansions in following cases:                              #
            #  -----------------------------------                              #
            #            1) value of state is stored in memo                    #
            #            2) time of expansion has expired                       #
            #            3) max depth has been reached out                      #
            #            4) reach terminal state                                #
            #-------------------------------------------------------------------#
            if mem_state in self.mem:
                return self.mem[mem_state]
            if state.terminal_test(): 
                return state.utility(self.player_id)
            if depth <= 0 or time.time() - self.start > self.EXPAND_TIMEOUT : 
                return heuristic(state)


            value = float("inf")

            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            self.mem[mem_state] = value                 
            return value

        def max_value(state, depth, alpha, beta):
            
            # memorization state used as a key 
            mem_state = (state.board,state.locs[0],state.locs[1],state.player())
           
            #-------------------------------------------------------------------#
            #  stop expansions in following cases:                              #
            #  -----------------------------------                              #
            #            1) value of state is stored in memo                    #
            #            2) time of expansion has expired                       #
            #            3) max depth has been reached out                      #
            #            4) reach terminal state                                #
            #-------------------------------------------------------------------#
            if mem_state in self.mem:
                return self.mem[mem_state]
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0 or time.time() - self.start > self.EXPAND_TIMEOUT:
                return heuristic(state)
            value = float("-inf")

            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            self.mem[mem_state] = value        
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1, float("-inf"), float("inf")))


    
    def minimax_ab(self, state, depth, heuristic):

        """
            Game-playing agent that chooses a move using your evaluation function
            and a depth-limited minimax algorithm with alpha-beta pruning, agent expand 
            nodes when time is below expansion time which is 0.1 sec.
            
            Parameters
            ----------

            - heuristic : used to calculate value od state based on certain heuristic

            - state : current state that of the game

            - depth : max depth of search tree 

        """

        def min_value(state, depth, alpha, beta):

            
            #-------------------------------------------------------------------#
            #  stop expansions in following cases:                              #
            #  -----------------------------------                              #
            #            1) time of expansion has expired                       #
            #            2) max depth has been reached out                      #
            #            3) reach terminal state                                #
            #-------------------------------------------------------------------#
            if state.terminal_test(): 
                return state.utility(self.player_id)
            if depth <= 0 or time.time() - self.start > self.EXPAND_TIMEOUT : 
                return heuristic(state)


            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break           
            return value

        def max_value(state, depth, alpha, beta):
            
            #-------------------------------------------------------------------#
            #  stop expansions in following cases:                              #
            #  -----------------------------------                              #
            #            1) time of expansion has expired                       #
            #            2) max depth has been reached out                      #
            #            3) reach terminal state                                #
            #-------------------------------------------------------------------#
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0 or time.time() - self.start > self.EXPAND_TIMEOUT:
                return heuristic(state)
            
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break      
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1, float("-inf"), float("inf")))
    