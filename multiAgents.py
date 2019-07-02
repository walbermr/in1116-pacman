# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class RuleAgent(Agent):
  def getAction(self, gameState):
    "*** OUR CODE HERE MAGO ***"
    util.raiseNotDefined()

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, pacManAction):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(pacManAction)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newFoodList = newFood.asList()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodNum = currentGameState.getFood().count()
    if len(newFood.asList()) == foodNum:  # if this action does not eat a food 
        dis = 1000000000
        for pt in newFood.asList():
            if manhattanDistance(pt , newPos) < dis :
                dis = manhattanDistance(pt, newPos)
    else:
        dis = 0
    for ghost in newGhostStates:  # the impact of ghost surges as distance get close
        dis += 4 ** (2 - manhattanDistance(ghost.getPosition(), newPos))
    return -dis

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      currGameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      currGameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      currGameState.getNumAgents():
        Returns the total number of agents in the game
    """
    depth = 0
    return self.getMaxValue(gameState, depth)[1]

  def getMaxValue(self, gameState, depth, agent = 0):
    actions = gameState.getLegalActions(agent)

    if not actions or gameState.isWin() or depth >= self.depth:
      return self.evaluationFunction(gameState), Directions.STOP

    successorCost = float('-inf')
    successorAction = Directions.STOP

    for action in actions:
      successor = gameState.generateSuccessor(agent, action)

      cost = self.getMinValue(successor, depth, agent + 1)[0]

      if cost > successorCost:
        successorCost = cost
        successorAction = action

    return successorCost, successorAction

  def getMinValue(self, gameState, depth, agent):
    actions = gameState.getLegalActions(agent)

    if not actions or gameState.isLose() or depth >= self.depth:
      return self.evaluationFunction(gameState), Directions.STOP

    successorCost = float('inf')
    successorAction = Directions.STOP

    for action in actions:
      successor = gameState.generateSuccessor(agent, action)

      cost = 0

      if agent == gameState.getNumAgents() - 1:
          cost = self.getMaxValue(successor, depth + 1)[0]
      else:
          cost = self.getMinValue(successor, depth, agent + 1)[0]

      if cost < successorCost:
          successorCost = cost
          successorAction = action

    return successorCost, successorAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    depth = 0
    return self.getMaxValue(gameState, depth)[1]

  def getMaxValue(self, gameState, depth, agent = 0):
    actions = gameState.getLegalActions(agent)

    if not actions or gameState.isWin() or depth >= self.depth:
      return self.evaluationFunction(gameState), Directions.STOP

    successorCost = float('-inf')
    successorAction = Directions.STOP

    for action in actions:
      successor = gameState.generateSuccessor(agent, action)

      cost = self.getMinValue(successor, depth, agent + 1)[0]

      if cost > successorCost:
          successorCost = cost
          successorAction = action

    return successorCost, successorAction

  def getMinValue(self, gameState, depth, agent):
    actions = gameState.getLegalActions(agent)

    if not actions or gameState.isLose() or depth >= self.depth:
      return self.evaluationFunction(gameState), None

    successorCosts = []

    for action in actions:
      successor = gameState.generateSuccessor(agent, action)

      cost = 0

      if agent == gameState.getNumAgents() - 1:
        cost = self.getMaxValue(successor, depth + 1)[0]
      else:
        cost = self.getMinValue(successor, depth, agent + 1)[0]

      successorCosts.append(cost)

    return sum(successorCosts) / float(len(successorCosts)), None

def betterEvaluationFunction(currGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

