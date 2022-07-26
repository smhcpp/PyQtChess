from Utilities import *

class Piece:
  """
    An abstract class which represents chess pieces
    
    ...

    Attributes:
    -----------
      ptype:int
        the type of the pieces: pawn=0, knight=1, bishop:2, rook=3, queen=4, king=5

    Methods:
    -----------
      getAvailableMoves():
        returns all available option specificly for this piece!
  """

  ptype=None
  pcolor=None
  position=None
  
  def __init__(self):
    pass

  def getAvailableMoves(self,pieces):
    pass

  #returns the same result as getAvailableMoves unless the piece is a Pawn or a King
  def getAvailableAttacks(self,pieces):
    pass
  
  def fakemove(self,topos):
    #print("From "+str(self.position)+" to "+str(topos))
    self.position=topos

  def move(self,topos):
    #print("From "+str(self.position)+" to "+str(topos))
    self.position=topos

class Pawn(Piece):
  def __init__(self,pcolor,position):
    self.ptype=0
    self.pcolor=pcolor
    self.position=position

  def getAvailableMoves(self,pieces):
    pmoves=list()
    step=(-1)**(self.pcolor+1)
    j=self.position[1]+step
    nkey=(self.position[0],j)
    # 1 step forward
    if not nkey in pieces:
      pmoves.append(nkey)
      # moving forward two steps:
      k=self.position[1]+2*step
      nkey=nkey=(self.position[0],k)
      if self.position[1]==6-self.pcolor*5 and not nkey in pieces:
        pmoves.append(nkey)

    # enpassant:
    
    #if self.enpassant!=None:
    #  if self.position[0] in [self.enpassant[0]+1,self.enpassant[0]-1] and self.position[1]==self.enpassant[1]:
    #    pmoves.append((self.enpassant[0],j))
        
        #  self.enpassantto=(self.enpassant[0],j)

    # taking:
    for r in [-1,1]:
      i=self.position[0]+r
      nkey=(i,j)
     
      if nkey in pieces:
        if pieces[nkey].pcolor!=self.pcolor:
          pmoves.append(nkey)
    return pmoves
  
  def getAvailableAttacks(self,pieces):
    step=(-1)**(self.pcolor+1)
    return [(self.position[0]+1,self.position[1]+step),(self.position[0]-1,self.position[1]+step)]

class Knight(Piece):
  def __init__(self,pcolor,position):
    self.ptype=1
    self.pcolor=pcolor
    self.position=position

  def getAvailableMoves(self,pieces):
    return getKnightMoves(pieces, self)  

  def getAvailableAttacks(self,pieces):
    return getKnightMoves(pieces, self) 

class Bishop(Piece):
  def __init__(self,pcolor,position):
    self.ptype=2
    self.pcolor=pcolor
    self.position=position

  def getAvailableMoves(self, pieces):
    return getDiagonalMoves(pieces, self)

  def getAvailableAttacks(self,pieces):
    return getDiagonalMoves(pieces, self) 

class Rook(Piece):
  def __init__(self,pcolor,position):
    self.ptype=3
    self.pcolor=pcolor
    self.position=position
    self.castlingright=True

  def move(self,topos):
    self.position=topos
    self.castlingright=False

  def getAvailableMoves(self,pieces):
    return getCardinalMoves(pieces, self)

  def getAvailableAttacks(self,pieces):
    return getCardinalMoves(pieces, self) 

class Queen(Piece):
  def __init__(self,pcolor,position):
    self.ptype=4
    self.pcolor=pcolor
    self.position=position

  def getAvailableMoves(self,pieces):
    pmoves=getCardinalMoves(pieces, self)
    pmoves.extend(getDiagonalMoves(pieces,self))
    return pmoves

  def getAvailableAttacks(self,pieces):
    return self.getAvailableMoves(pieces)

class King(Piece):
  def __init__(self,pcolor,position):
    self.ptype=5
    self.pcolor=pcolor
    self.position=position
    self.castlingright=True

  def move(self,topos):
    self.position=topos
    self.castlingright=False


  def getAvailableAttacks(self, pieces):
    return getKingAttacks(pieces, self)
  
  def getAvailableMoves(self, pieces):
    pmoves=getKingAttacks(pieces, self)
    pmoves.extend(getKingCastlingMoves(pieces, self))
    return pmoves

