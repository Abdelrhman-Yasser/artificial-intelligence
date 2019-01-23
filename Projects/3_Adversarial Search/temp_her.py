def keep_enemy_near_h(self, state):
        """
            - This heuristic follows "keep your enemies closer" .
            
            - Idea : player will choose action that make him near to obstacle
            
            - Equation : manhattan distances from enemy player

            - Analysis : 20.2%                            
        """
        def cal(matrix):
            total = 0 
            px = 0
            py = 0
            ex = 0
            ey = 0
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == -1:
                        px = i
                        py = j
                    if matrix[i][j] == 2:
                        ex = i
                        ey = j
                                
            total = self.manhattan_dist((px,py), (ex,ey))

            return total                         

        if(state.is_winner()):
            return float("inf")
        if(state.terminal_test()):
            return float("-inf")    
        return cal(state.obstacles_matrix())    

    def away_from_obstacles_h(self, state):
        """
            - This heuristic says that if player is away from obstacles it's better situation for him and therefore could lead to win.
            
            - Idea : player will choose action away from obstacles
            
            - Equation : - manhattan distances from all obstacles

            - Analysis : 30.2%                            
        """
        def cal(matrix):
            total = 0 
            ox = 0
            oy = 0    
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == -1:
                        ox = i
                        oy = j
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 1:
                        total += self.manhattan_dist((ox,oy), (i,j))
            return total      
        
        if(state.is_winner()):
            return float("inf")
        if(state.terminal_test()):
            return float("-inf")
        return -cal(state.obstacles_matrix()) 


    def keep_near_center_away_obstacles_h(self, state):
        """
                - Analysis : 54.0%        
        """

        NEAR_THRESHOLD = 4
        AWAY_THRESHOLD = 10
        AVERAGE_GAME_COUNT = 90

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


            
            obstacles_player = 0            
            obstacles_enemy = 0 
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 1:
                        dis_player = self.manhattan_dist((px,py), (i,j))
                        if NEAR_THRESHOLD <= dis_player <= AWAY_THRESHOLD:
                            obstacles_player += 1 
                        dis_enemy = self.manhattan_dist((ex,ey), (i,j))
                        if NEAR_THRESHOLD <= dis_enemy <= AWAY_THRESHOLD:
                            obstacles_enemy += 1
            

            d1 = self.manhattan_dist((ex,ey), (cx,cy)) 
            d2 = self.manhattan_dist((px,py), (cx,cy))                  

            print(cx,cy)
            print(d1)
            print(d2)
                                    

            near_center = self.manhattan_dist((ex,ey), (cx,cy)) - self.manhattan_dist((px,py), (cx,cy))
            total = -obstacles_player

            if state.ply_count < 25:
                total += near_center
            
            return total                       
        print(DebugState.from_state(state))    
        if(state.is_winner()):
            return float("inf")
        if(state.terminal_test()):
            return float("-inf")    
        x = self.zero_sum_h(state)
        y = 0 

        if x == 0: 
            if state.ply_count < 25:
                y = cal(state.obstacles_matrix())
            
        print(state.ply_count)
        print(x,y)
        print(x+y)
        return x + y     