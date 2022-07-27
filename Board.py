from Utilities import *
from Piece import *
from math import floor

class Board:
  pieces=dict()
  kingpositions=dict()
  #castlingrights=[[True,True],[True,True]]
  #ischecked=[False,False]
  enpassantready=None
  #enpassantto=None
  movesnumber=0

  def __init__(self):
    self.setUpPieces()

  def setUpPieces(self):
    for pcolor in range(2):
      for i in range(8):
        boardpos=(i,ypospawn[pcolor])
        p=Pawn(pcolor,boardpos)
        self.pieces[boardpos]=p

      ##print("Pawns are done!")
      
      for i in xpositions[1]:
        boardpos=(i,yposothers[pcolor])
        ##print(self.colornames[pcolor]+" "+self.typenames[ptype]+" at "+str(boardpos))
        p=Knight(pcolor,boardpos)
        self.pieces[boardpos]=p

      for i in xpositions[2]:
        boardpos=(i,yposothers[pcolor])
        p=Bishop(pcolor,boardpos)
        self.pieces[boardpos]=p

      for i in xpositions[3]:
        boardpos=(i,yposothers[pcolor])
        p=Rook(pcolor,boardpos)
        self.pieces[boardpos]=p

      for i in xpositions[4]:
        boardpos=(i,yposothers[pcolor])
        p=Queen(pcolor,boardpos)
        self.pieces[boardpos]=p

      for i in xpositions[5]:
        boardpos=(i,yposothers[pcolor])
        p=King(pcolor,boardpos)
        self.kingpositions[pcolor]=boardpos
        self.pieces[boardpos]=p

  def islegal(self, frompos,topos):
    flag=True
    pcolor=self.pieces[frompos].pcolor
    kingpos=self.kingpositions[pcolor]
    reversecastlingright=False
    if self.pieces[frompos].ptype==5:
      kingpos=topos
      reversecastlingright=self.pieces[frompos].castlingright

    if self.pieces[frompos].ptype==3:
      reversecastlingright=self.pieces[frompos].castlingright

    temp=None
    if topos in self.pieces:
      temp=self.pieces[topos]
      del self.pieces[topos]

    self.pieces[topos]=self.pieces[frompos]
    self.pieces[topos].move(topos)
    del self.pieces[frompos]

    #updating next possible fake moves:
    
    checkingpieces=getCheckingPieces(self.pieces,kingpos,pcolor)
    #  #print(self.typenames[self.pieces[k].ptype]+" at "+str(self.getsquareuarename(k))+" is checking the squareuare "+self.getsquareuarename(kingpos))
    if len(checkingpieces)>0:
      flag=False
    
    #reversing the fake move
    self.pieces[frompos]=self.pieces[topos]
    self.pieces[frompos].move(frompos)
    del self.pieces[topos]
    if reversecastlingright:
      self.pieces[frompos].castlingright=True
    if temp!=None:
      self.pieces[topos]=temp

    return flag

  def iscastlingpossible(self,pieces,topos,pcolor):
    side=1-floor(topos[0]/4) #kingside is zero and queenside 1
    for i in range(4,4+2*(-1)**side):
      square=(i,yposothers[pcolor]) 
      if len(getcheckingpieces(pieces, square, pcolor))>0:
        return False
      if i!=4: 
        if square in pieces:
          return False
          
    return self.castlingrights[pcolor][side]

  def isForcedDraw(self):
    #check stalemate
    if len(self.pieces)<3:
      return True
    if len(self.pieces)==3:
      for k in self.pieces:
        if self.pieces[k].ptype in [1,2]:
          return True
    return False

  def move(self,frompos,topos):
    """
    returns:
      0: a normal move where nothing has to be done! 
      1: TODO: a check mate! (find who is mated by movenumber)
      2: TODO: a Stalemate! (find who stalemated by movenumber)
      3: a draw by insufficient materials
      4: TODO: a draw by repetition of moves
      10: promotion
      11: castling
      12: enpassant
      404: ilegal move!
    """
    #if self.isForcedDraw():
    #  return 3
    enpassantflag=False
    piece=self.pieces[frompos]
    cond1= topos[0] in range(8) and topos[1] in range(8)
    cond2= piece.pcolor==self.movesnumber%2
    if cond1 and cond2:
      pmoves=piece.getAvailableMoves(self.pieces)
      if piece.ptype==0 and self.enpassantready!=None:
        #make enpassant a possible move
        cond01=abs(frompos[0]-self.enpassantready[0])==1 and frompos[1]==self.enpassantready[1]
        cond02=topos[0]==self.enpassantready[0] and topos[1]==self.enpassantready[1]+(-1)**(piece.pcolor+1)
        if cond01 and cond02:
          pmoves.append(topos)
          enpassantflag=True
      if topos in pmoves:
        enpassantready_temp=self.enpassantready
        self.enpassantready=None
        if self.islegal(frompos,topos):
          self.movesnumber+=1
          #maybe self.pieces.pop(topos)!!!
          self.pieces[topos]=self.pieces[frompos]
          self.pieces[topos].move(topos)
          self.pieces.pop(frompos)
          if self.pieces[topos].ptype==0:
            if enpassantflag:
              self.pieces.pop(enpassantready_temp)
              return 12
            if abs(topos[1]-frompos[1])==2:
              self.enpassantready=topos
            if self.pieces[topos].position[1]==7-yposothers[self.pieces[topos].pcolor]:
              return 10
          elif self.pieces[topos].ptype==5:
            self.kingpositions[self.pieces[topos].pcolor]=topos
            if abs(frompos[0]-topos[0])==2 and frompos[1]==topos[1]:
              side=floor(topos[0]/4) #0:queenside, 1:kingside
              rookx=7*side
              rooktox=topos[0]+(-1)**side
              self.pieces[(rooktox,topos[1])]=self.pieces[(rookx,topos[1])]
              self.pieces.pop((rookx,topos[1]))
              self.pieces[(rooktox,topos[1])].move((rooktox,topos[1]))
              return 11
          return 0
    return 404

  def takeFurtherActions(self,action):
    if action[0]==10: #complete the promotion process!
      #action: [10,ptype,topos]
      if action[1]==1:
        p=Knight(self.pieces[action[2]].pcolor,action[2])
        self.pieces.pop(action[2])
        self.pieces[action[2]]=p
      elif action[1]==2:
        p=Bishop(self.pieces[action[2]].pcolor,action[2])
        self.pieces.pop(action[2])
        self.pieces[action[2]]=p
      elif action[1]==3:
        p=Rook(self.pieces[action[2]].pcolor,action[2])
        self.pieces.pop(action[2])
        self.pieces[action[2]]=p
      elif action[1]==4:
        p=Queen(self.pieces[action[2]].pcolor,action[2])
        self.pieces.pop(action[2])
        self.pieces[action[2]]=p


    """

  #enpassant part:
  enpassantover=self.board.enpassant
  enpassantto=self.board.enpassantto
  self.board.enpassant=None
  self.board.enpassantto=None
  self.board.beingchecked[obj.pcolor]=False
  if self.board.pieces[self.selectedlabelpos].ptype==0:
      if abs(topos[1]-self.selectedlabelpos[1])==2:
          self.board.enpassant=topos
      elif enpassantto!=None and topos[0]==enpassantto[0] and topos[1]==enpassantto[1]:
          self.board.pieces[enpassantover].close()
          del self.board.pieces[enpassantover]
          del self.board.pieces[enpassantover]
  """

  def __str__(self):
    buffer=""
    for i in range(8):
      buffer += "|"
      for j in range(8):
        k=(j,i)
        if k in self.pieces:
          buffer+=ptypeabbr[self.pieces[k].ptype]+"|"
        else:
          buffer+=" |"
      buffer+="\n"
    return buffer
