from math import floor


columnnames=['a','b','c','d','e','f','g','h']
ptypenames=["Pawn","Knight","Bishop","Rook","Queen","King"]
ptypeabbr=["P","N","B","R","Q","K"]
pcolornames=["White","Black"]
ypospawn=[6,1]
yposothers=[7,0]
xpositions=[range(8),[1,6],[2,5],[0,7],[3],[4]]


def getSquareName(elem):
  return columnnames[elem[0]]+str(8-elem[1])

def getCheckingPieces(pieces,square,pcolor):
  checkingpieces=dict()
  for k in pieces:
    if pieces[k].pcolor !=pcolor:
      temp=pieces[k].getAvailableAttacks(pieces)
      if square in temp:
        checkingpieces[k]=square
  return checkingpieces

def isCastlingPossible(pieces,topos,piece):
  side=1-floor(topos[0]/4) #kingside is zero and queenside 1
  key=(7-side*7,piece.position[1]) #rook must be in this position

  if key not in pieces:
    return False
  if pieces[key].ptype!=3:
    return False
  step=(-1)**side
  for i in range(4,4+3*step,(-1)**side):
    square=(i,piece.position[1]) 
    if len(getCheckingPieces(pieces, square, piece.pcolor))>0:
      return False
    if i!=4: 
      if square in pieces:
        return False

  return piece.castlingright and pieces[key].castlingright

def getKingAttacks(pieces,piece):
  steps=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
  pmoves=list()
  for r in steps:
    i=piece.position[0]+r[0]
    j=piece.position[1]+r[1]
    if i in range(8) and j in range(8):
      nkey=(i,j)
      if nkey in pieces:
        if pieces[nkey].pcolor!=piece.pcolor:
          pmoves.append(nkey)
      else:
        pmoves.append(nkey)
  return pmoves

def getKingCastlingMoves(pieces,piece):
    pmoves=list()
    csteps=[-2,2]
    for s in csteps:
      nkey=(4+s,piece.position[1])
      if isCastlingPossible(pieces,nkey , piece):
        pmoves.append(nkey)
    return pmoves

def getDiagonalMoves(pieces,piece):
  steps=[-1,1]
  pmoves=list()
  for r in steps:
    for s in steps:
      i=piece.position[0]+r
      j=piece.position[1]+s
      while i in range(8) and j in range(8):
        nkey=(i,j)
        if nkey in pieces:
          if pieces[nkey].pcolor!=piece.pcolor:
            pmoves.append(nkey)
          break
        else:
          pmoves.append(nkey)
        i+=r
        j+=s
  #print(pmoves)
  return pmoves  

def getCardinalMoves(pieces,piece):
  steps=[-1,1]
  pmoves=list()
  for r in steps:
    i=piece.position[0]+r
    j=piece.position[1]
    while i in range(8) and j in range(8):
      nkey=(i,j)
      if nkey in pieces:
        if pieces[nkey].pcolor!=piece.pcolor:
          pmoves.append(nkey)
        break
      else:
        pmoves.append(nkey)
      i+=r

    i=piece.position[0]
    j=piece.position[1]+r
    while i in range(8) and j in range(8):
      nkey=(i,j)
      if nkey in pieces:
        if pieces[nkey].pcolor!=piece.pcolor:
          pmoves.append(nkey)
        break
      else:
        pmoves.append(nkey)
      j+=r
  return pmoves

def getKnightMoves(pieces,piece):
  steps=[[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
  pmoves=list()
  for r in steps:
    i=piece.position[0]+r[0]
    j=piece.position[1]+r[1]
    if i in range(8) and j in range(8):
      nkey=(i,j)
      if nkey in pieces:
        if pieces[nkey].pcolor!=piece.pcolor:
          pmoves.append(nkey)
      else:
        pmoves.append(nkey)
  return pmoves