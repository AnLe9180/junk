import random
import math
import operator
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=.1):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor
        self.n_test = 0
        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed


    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """
        self.planner.route_to(destination)
        self.n_test= self.n_test+1
        if testing==True:
            self.alpha=0
            self.epsilon=0
        if testing==False:
        # Select the destination as the new location to route to

            self.alpha += 0.005
            if (self.alpha < 0):
                self.alpha = 0
            if (self.alpha > 1):
                self.alpha = 1
            ########### 
            ## TO DO ##
            ###########
            # Update epsilon using a decay function of your choice
            # Update additional class parameters as needed
            # If 'testing' is True, set epsilon and alpha to 0
    #        self.epsilon = (self.epsilon-.05)
            #self.epsilon = pow(self.alpha,self.n_test)
            self.epsilon=math.exp(-.01*self.alpha*self.n_test)
            if (self.epsilon < 0):
                self.epsilon = 0
            
        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent   
#        state = ()
#        for x,y in inputs.items():
#            state = state + (y,)
#            #print state
#        state =  (self.next_waypoint,)    + state[:2]
        state = (waypoint, inputs['light'], inputs['oncoming'])
        #print state, "HOLA",
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state
        
        maxQ=-10000000000000000000000000000
        for states in self.Q:

                if states == state:
                    #print "2", state
                    #print "2",current_state, qtable[(state)], actions
                    for actions in self.valid_actions:
                        if maxQ <=  self.Q[(states)][actions]:
                            maxQ=self.Q[(states)][actions]
        #print "maxQ :", maxQ
                    #print 'I CHOSE PURPOSEFULLY'


        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if self.learning == True:
            if state not in self.Q:
                self.Q[(state)] = dict()
                for action in self.valid_actions: 
                    self.Q[(state)][action] = 0
        #print self.Q[(state)], state
        return 


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        rando = random.uniform(0,1)
        #rando=.35
        #rando = random.uniform(.1, .3)
        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
        if not self.learning:
            action = random.choice(self.valid_actions)
        else:
            for states in self.Q:
                for actions in self.valid_actions:
                    if states == state and self.epsilon > rando:
                        #print random.randrange(0,1)
                        #print "2", state
                        #print "2",current_state, qtable[(state)], actions
                        action= random.choice(self.valid_actions)
        
                        #print 'I CHOSE EXPLORATATIVELY'
                    if states == state and self.Q[(states)][actions] == self.get_maxQ(state):
                        #print "2", state
                        #print "2",current_state, qtable[(state)], actions
                        equal_act = []
                        equal_act.append(actions)
                        action = random.choice(equal_act)
                        
                    if states == state and self.Q[(states)][actions] > self.get_maxQ(state):
                        #print "2", state
                        #print "2",current_state, qtable[(state)], actions
                        
                        action = actions
                        #print self.Q[(states)][action], self.get_maxQ(state),'I CHOSE PURPOSEFULLY'
                        #print 'I CHOSE PURPOSELY'
#                    if states == state and self.get_maxQ(state) < 0:
#                        print "AYYYYY",range(self.valid_actions)
#                        action= random.choice(self.valid_actions)
        #print "RANDOM:", rando
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
#        nextpt = self.planner.next_waypoint() 
#        inputs = self.env.sense(self)
#        nxstate = ()
#        for x,y in inputs.items():
#            nxstate = nxstate + (y,)
#            #print x,y
#            #print state
#        nxstate =  (self.next_waypoint,)    + state[:2]
        self.createQ(state)
#        self.createQ(nxstate)
        #print action, nxstate, state,"HOLA@", self.Q[(state)][action]

        self.Q[(state)][action] = (1-self.alpha)*(self.Q[(state)][action])+self.alpha*(reward)

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning=True)
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=.00001, display=False, log_metrics=True)
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=10)
    
    print "END"


if __name__ == '__main__':
    run()
