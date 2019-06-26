# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
import bfs

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index
    self.prob_scared_flee = 0.99
    self.prob_attack = 0.99

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0: 
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )
    
  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()

class RuleGhost( GhostAgent ):

  def __chokeSearch(self, state, visited, queue):
    directions = [(0,1), (0,-1), (1, 0), (-1, 0)]
    choke_points = []

    while len(queue) > 0:
      p = queue.pop(0)
      possibilities = []
      
      for d in directions:
        new_point = (p[0] + d[0], p[1] + d[1])
        is_legal = bfs.testLegal(state.getWalls(), new_point)

        if is_legal and new_point not in visited:
          possibilities.append(new_point)
          
      if len(possibilities) > 1:
        choke_points.append(visited[len(visited) - 1])
      elif len(possibilities) > 0:
        queue.append(possibilities[0])

      visited.append(p)
    
    return choke_points

  def getChockingPoints(self, state):
    starting_point = state.getPacmanPosition()
    possible_sorroundings = []
    directions = [(0,1), (0,-1), (1, 0), (-1, 0)]

    for d in directions:
      x = starting_point[0] + d[0]
      y = starting_point[1] + d[1]
      if bfs.testLegal(state.getWalls(), (x,y)):
        possible_sorroundings.append((x,y))
    
    # print 'choke - ' self.__chokeSearch(state, [starting_point], possible_sorroundings))
    return self.__chokeSearch(state, [starting_point], possible_sorroundings)

  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    choke_points = self.getChockingPoints(state)
    target_point = None

    if len(choke_points) > 1:
      target_point = choke_points[self.index - 1]
    else:
      target_point = state.getPacmanPosition()
    
    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( int(pos[0]+a[0]), int(pos[1]+a[1]) ) for a in actionVectors]

    # Select best actions given the state

    distancesToTarget = [ len(bfs.search(pos, target_point, state.getWalls())) for pos in newPositions]

    if isScared:
      bestScore = max( distancesToTarget )
      bestProb = self.prob_scared_flee
    else:
      bestScore = min( distancesToTarget )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToTarget ) if distance == bestScore]
    
    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
    dist.normalize()
    return dist
  
class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
      
  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0
    
    speed = 1
    if isScared: speed = 0.5
    
    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    else:
      bestScore = min( distancesToPacman )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]
    
    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
    dist.normalize()
    return dist
