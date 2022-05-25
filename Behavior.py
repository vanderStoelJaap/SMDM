from tkinter import END
from turtle import end_fill
from Shapes import features


class behavior:
  
  def skills():
    avoid = {"id" : "avoid"}
    noEnter = {"id" : "noEnter"} # Necessary? 
    avoidPass = {"id" : "avoidPass"}
    Move = {"id" : "Move"}
    Dribble = {"id" : "Dribble"}
    HumanDribble = {"id" : "HumanDribble"}
    Shoot = {"id" : "Shoot"}
    Pass = {"id" : "Pass"}
    Target = {"id" : "Target"} # Necessary? 

  def semantics():
     
    avoidOpponentWide = []

    avoidOpponentNarrow = []
      for opponents in features.opponent:
    
    field = [] 

    givepass = []

    dribble = []

    shoot = []

