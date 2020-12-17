import sys, getopt, os, re
#                                     ORG 0000100
a = 0                               #
b = 0                               #
d = 0                               #
#                                           0 67 MAIN               ; Goto Main
#                                                                   ; 
#                                                                   ;  -------------
#                                                                   ; |  Constants  |
#                                                                   ;  -------------
const1 = 1                          # C1:   0000001                 ; Constant for 1
const2 = 2                          # C2:   0000002                 ; Constant for 2
constGridSize = 9                   # CG:   0000011                 ; Constant for Game Grid Size - 9 ( 11[8] ) 
playLength = 24                     # CPL:  0000030                 ; Constant for Plays List Length - 24 ( 30[8] )
tupleLength = 3                     # CTL:  0000003                 ; Constant for Play Length  - 3
playsGridPointer = 0                # _PL:  CP                      ; Constant Pointer to Plays List
#                                                                   ; Constant Plays List
plays = [0,1,2,3,4,5,6,7,8,         # CP:   0000000                 ; - Play 1
        0,3,6,1,4,7,2,5,8,          #       0000001   
        0,4,8,2,4,6]                #       0000002
#                                           0000003                 ;  - Play 2
#                                           0000004
#                                           0000005
#                                           0000006                 ;  - Play 3
#                                           0000007
#                                           0000000     
#                                           0000010                 ;  - Play 4
#                                           0000003
#                                           0000006
#                                           0000001                 ;  - Play 5
#                                           0000007
#                                           0000004
#                                           0000002                 ;  - Play 7
#                                           0000005
#                                           0000010
#                                           0000000                 ;  - Play 8
#                                           0000004     
#                                           0000010
#                                           0000002                 ;  - Play 9
#                                           0000004     
#                                           0000006 
patternDraw0= 5252525               # CPD0: 5252525                 ; Constant Alternating Lamp Pattern For Draw - 0
patternDraw1= 2525252               # CPD1: 2525252                 ; Constant Alternating Lamp Pattern For Draw - 1
displayDelay= 3777775               # CDD:  3777775                 ; Maximum Positive value for delay
#                                                                   ;
#                                                                   ;  -----------------
#                                                                   ; |   Variables     |
#                                                                   ;  -----------------
moved = 0                           # VM:   0000000                 ; V Moved flag - indicating a move was completed
gridPointer = 0                     # _GP:  VGRD                    ; V Pointer to Game Grid
grid = [0,0,0, 0,0,0, 0,0,0]        # VGRD: 0000000                 ; V Game Grid 
#                                           0000000
#                                           0000000
#                                           0000000
#                                           0000000
#                                           0000000
#                                           0000000
#                                           0000000
#                                           0000000
currentPlayPointer = 0              # _CP:  0000000                 ; V Pointer to the Current Play array                             
currentPlay = [0,0,0]               # VPLY: 0000000                 ; V Current Play array
#                                           0000000
#                                           0000000
playIndex = 0                       # VPX:  0000000                 ; V Index of Current Play in the Play List
cellIndex = 0                       # VCX:  0000000                 ; V Index of the Cell in the Game Grid
tupleIndex = 0                      # VTX:  0000000                 ; V Index of Current Play cell
emptyIndex = -1                     # VEX:  3777777                 ; V Index of Last Empty Game Grid Cell 
threatCount = -1                    # VTC:  3777777                 ; V Threat count 
advantageCount = -1                 # VAC:  3777777                 ; V Advantage count
turn = 0                            # VTN:  0000000                 ; V Whose turn indicator ( 0 == Player )
lastMove = -1                       # VLM:  3777777                 ; V Game Grid address of last move
switches = 1                        #                               ; V Console Switch Value
moveType = -1                       # MVT:  3777777                 ; V Which type of move evaluation to perform


def main(argv):                     # MAIN: 0000000                 ; MAIN procedure ======================================================
    global switches, turn, moved    #                               ; >> Read 1 from Console Switches indicating play moves first << ------
    global d, a                     #                               ; >> If player moves first, gosub playerFirstMove.            << ------
    #                                                               ; >> Continue by starting Play procedure,                     << ------
    switches = 1                    #                               ;    Emulate initial swich position as 1
    #                                       0 76 C1                 ;    Set IO to C1 (1 - Switches)
    d = switches                    #       0 04 1                  ;    Set D <- IO
    if d != 0: playerFirstMove()    #       0 61 MA0                ;    If D != 0 Goto MA0 ( MAIN SubRoutine link  0 )
    #                                       0 67 MN0                ;    Else Goto MN0 ( MAIN Subroutine Link 1 )
    #                                 MA0:  0 57 PFM                ;    MA0: GoSub PFM (playerFirstMove)
    play()                          # MN0:  0 67 PLAY               ;    MN0: GOTO PLAY
    #                                                               ; ======================================================================


def play():                         # PLAY: 0000000                 ; PLAY procedure =======================================================
    global d, turn                  #                               ; >> Endless loop evaluating the turn variable, and calling   << -------
    #                                                               ; >> computer or player to take a move.  Outcomes are tested  << -------
    while True:                     #                               ; >> within the moves, causing an escape from the loop.       << -------
        d = turn                    # LPLY: 0 30 VTN                ;    LPLY: get D <- VTN (turn)        This is the loop start
        if d > 0: playerPlay()      #       0 62 PL0                ;          If D > 0 goto PL0 (subroutine link 0 for playerPlay)    
        else: computerPlay()        #       0 57 CPLA               ;          Else link CPLA (Procedure computerPLays) 
        #                                   0 67 PLN1               ;          Skip over PL0 subroutine link 0
        #                             PL0:  0 57 PPLA               ;          link PPLA (playerPlays)
        #                             PLN1: 0 67 LPLY               ;          Goto LPLY (loop)     
    #                                                               ; ======================================================================


def playerPlay():                   # PPLA: 0000000                 ; PPLA (playerPlay) procedure ==========================================
    #                                                               ; >> Waits for input, then checks to see if the game is over. << =======
    awaitMove()                     #       0 57 AWMV               ;    link AWMV ( await player move )
    isDraw()                        #       0 57 IDRW               ;    link IDRW ( check for game over )
    return                          #       0 67 PPLA               ;    Return via PPLA
    #                                                               ; ====================================================================== 
       

def computerPlay():                 # CPLA: 0000000                 ; CPLA (computerPLay) procedure ========================================
    #                                                               ; >> Computer calculates move.  If it wins with the move it   << =======
    #                                                               ; >> jumps to a the 'win' procedure.  Otherwise tests for a   << =======
    #                                                               ; >> draw. If the draw returns, the it continues to showing   << =======
    #                                                               ; >> its move. The play loop will then await the player's     << =======
    #                                                               ; >> next play.
    move()                          #       0 57 MV                 ;    link MV (move)
    isDraw()                        #       0 57 IDRW               ;    link IDRW (isDraw)
    showMove()                      #       0 57 SHMV               ;    link SHMV (showMove)
    return                          #       0 67 CPLA               ;    Return via CPLA
    #                                                               ; ======================================================================


def awaitMove():                    # AWMV: 00000000                ; AWMV (awaitMove) procedure ===========================================
    global moved, d, grid, a, turn  #                               ; >> Sets up input, then breaks awaiting program restart.    << ========
    global lastMove                 #                               ; >> Once restarted the move is tested for validity. If      << ========                                                             
    #                                                               ; >> valid the move is recorded. Otherwise the system stops  << ========
    #                                                               ; >> for input again. It will loop until valid input is      << ========
    #                                                               ; >> received.                                               << ========
    while True:                     #    
        switches = int(                 
            input("move: "))        # LAMV: 1 76 C1                 ;    LAMV: set RSR <- C1 (1) indicating switches    Loop Start
        d = switches                #       0 04 1                  ;          get D <- IO 
        d = d - const1              #       0 32 C1                 ;          subtract D - C1 (1)     Decrement for zero indexing
        lastMove = d                #       0 34 VLM                ;          set D -> VLM (lastMove)
        d = d + gridPointer         #       0 31 _PL                ;          add D + _PL (playGridPointer) 
        #                                   0 71 1                  ;          indirect address next instruction to D
        a = grid[d]                 #       0 10 0                  ;          set A <- Value at D
        if a == 0: break            #       0 50 EAMV               ;          If A == 0 goto EAMV (break)    Zero confirms free 
        else: pass                  #       0 67 LAMV               ;          else goto LAMV (repeat loop)
    a = const1                      # EAMV: 0 10 C1                 ;    EAMV: get A <- C1 (1)   
    #                                       0 71 1                  ;    indirect address next instruction to D
    grid[d] = a                     #       0 10 0                  ;    set A -> Value at D
    a = 0                           #       0 27 0                  ;    Clear A
    turn = a                        #       0 14 VTN                ;    Set A -> VTN (turn)
    return                          #       0 67 AWMV               ;    goto AMVW (return)
    #                                                               ; ======================================================================


def move():                         # MV:   0000000                 ; MV (move) procedure ==================================================
    global currentPlay, d           #                               ; >> Completes 3 evaluation loops. In each loop it checks    << ========
    global turn, moved              #                               ; >> each play in the last against the game grid values.     << ========
    global playLength               #                               ; >> On the first pass it looks for a winning move.  On the  << ========
    global playIndex, moveType      #                               ; >> second it look to defend against player win.  On the    << ========
    #                                                               ; >> If a move wasn't selected on either pass so far, it     << ========
    #                                                               ; >> chooses the next available move.                        << ========
    #
    #                                                               ; >> Before executing its move, it resets the turn indicator.<< ========
    d = const1                      #       0 30 C1                 ;    get D <- C1 (1)
    turn = d                        #       0 34 VTN                ;    set D (1) -> VTN (turn)
    #
    #                                                               ; >> Initialise for evalution
    moved  = 0                      #       0 17 VM                 ;    clear VM (moved)
    d = playsGridPointer            #       0 30 _PL                ;    get D <- _PL (playsGridPointer)  
    d = d + playLength              #       0 31 CPL                ;    add D + CPL (playLength)
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    playIndex = d                   #       0 34 VPX                ;    set D -> VPX (playIndex)
    setCurrentPlay()                #       0 57 SCPY               ;    gosub SCPY (setCurrentPlay) 
    #
    #                                                               ; >> Set evaluation type indicator to -1 (advantage)
    d = 0                           #       0 27 1                  ;    clear D
    d = d - 1                       #       0 32 C1                 ;    subtract D - C1 (1)
    moveType = d                    #       0 34 MVT                ;    set D (-1) ->  MVT (moveType)
    #                                                               ;
    while True:                     #                               ;
        while True:                 #                               ;
            playMove()              # LMV1: 0 57 PLMV               ;    LMV1: gosub PLMV (playMove)
            #
            #                                                       ;           >> Did that result in a move? 
            d = moved               #       0 30 VM                 ;           set D <- VM (moved)
            if d != 0: return       #       0 61 MV                 ;           if D != 0 goto MV (return)
            #                                                       ;
            #                                                       ;           >> Decrement Index to Next Play <<-------------
            d = playIndex           #       0 30 VPX                ;           set D <- VPX (playIndex) 
            d = d - tupleLength     #       0 32 CTL                ;           subtract D - CTL (tupleLength)
            playIndex = d           #       0 34 VPX                ;           set D -> VPX (playIndex)
            #
            #                                                       ;           >> If we're out of plays end loop <<-------------
            if d < 0: break         #       0 63 EMV1               ;           if D < 0 goto EMV1 (Loop End)                                                           ; >> Else get the next Play <<
            setCurrentPlay()        #       0 57 SCPY               ;           gosub SCPY (setCurrentPlay)
        #                                   0 60 LMV1               ;           goto LMV1 (repeat loop)
        #                                                           ;
        #                                                           ;       >> Check for Moved 
        d = moved                   # EMV1: 0 30 VM                 ;       set D <- VM (Moved)
        if d != 0: return           #       0 61 VM                 ;       if d != 0 goto MV (return)
        #                                                           ;  
        #                                                           ;       >> Reset for next pass
        initPlayScan()              #       0 57 IPS                ;       GoSub IPS (initPlayScan)
        d = moveType                #       0 30 MVT                ;       Get D <- C1 (1)
        d = d + const1              #       0 31 C1                 ;       add D + C1 (1)
        moveType = d                #       0 34 MVT                ;       Set D (1) ->  MVT (moveType)
        d = d - const1              #       0 32 C1                 ;       subtract D - C1 (1)
        if d > 0: break             #       0 62 EMV2               ;       if d is positive goto EVM2 (break)  
        #                           #       0 67 LMV1               ;       goto LMV1 (repeat loop)     
        #                                                           ;           
    return                          # EMV2: 0 67 MV                 ;  goto MV (return)
    #                                                               ; ======================================================================    



def isDraw():                       # IDRW: 0000000                 ; IDRW (isDraw) procedure ==============================================  
    global turn                     #                               ; >> Scans all game grid cells to see if there are any left  << ========
    global a, d, constGridSize      #                               ; >> to play. If there aren't, a draw indicator is shown and << ======== 
    global gridPointer, playIndex   #                               ; >> the system stops. It then waits to be restrated. When   << ========
    global grid                     #                               ; >> restarted, it's the computer's turn. So the game state  << ========
    #                                                               ; >> is cleared, and the play procedure is run again.        << ========
    #                                                               ; 
    #                                                               ; >> Set cursor to start grid read
    d = gridPointer                 #       0 30 _PL                ;    get D <- _PL (play gridPointer)
    d = d + constGridSize           #       0 31 CG                 ;    add D + CG (constGridSize)
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    while True:                     #                               ;
        #                           # LDR0: 0 71 1                  ; LDR0: Modify next instruction with Address in D   LOOP
        a = grid[d]                 #       0 10 0                  ;       Set A <- value at D
        #                                                           ;       >> If grid cell is available continue game<<
        if a == 0: return           #       0 50 IDRW               ;       if A == 0 return IDRW
        #                                                           ;       >> else move cursor
        d = d - const1              #       0 32 C1                 ;       Subtract D - C1 (1) 
        a = d                       #       0 25 0                  ;       Copy D -> A
        a = a - gridPointer         #       0 12 _PL                ;       Subtract A - _PL (gridPointer)
        #                                                           ;       >> if last grid cell
        if a < 0: break             #       0 67 EDR0               ;       if A is NEGATIVE goto EDR0 (break) 
        #                                   0 67 LDR0               ;       goto LDR0 (repeate loop)  
    #                                                               ;
    #                                                               ; >> If we haven't already returned, then the board is full 
    #                                                               ; >> So we'll flash alterating patterns 9 times                             
    d = constGridSize               # EDR0: 0 30 CG                 ; EDR0: Set D <- CG (constantGridSize)              LOOP EXIT
    while True:                     #                               ;     
        #                             IDR1: 0 76 C2                 ; IDR1: Set IO to C2(2) -- lamps                   LOOP
        #                                   0 03 CPD0               ;       Output CPD0 (drawPattern0)
        #                                   0 72 CDD                ;       Count next word up to CDD (delay)
        #                                   00000000                ;       0
        #                                   0 03 CPD1               ;       Output CPD1 (drawPattern1)
        #                                   0 72 CDD                ;       Count next word up to CDD (delay)
        #                                   00000000                ;       0
        d = d - const1              #       0 32 C1                 ;       Subtract D - C1 (1)
        if d < 0: break             #       0 63 IDN0               ;       if D IS NEGATIVE goto IDN0 (break)
        else: pass                  #       0 67 IDR1               ;       Goto IDR1 (repeat)       
    #                                                               ;
    print("Draw")                   #                               ; >> Stop system awaiting new game.  When restarting the computer
    input("Push Start: ")           #                               ; >> will play first
    turn = 0                        # IDN0: 2 17 VTN                ; IDN0: Clear Turn and STOP                         LOOP EXIT
    newGame()                       #       0 57 NEW                ;    GoSub NEW (newGame)
    play()                          #       0 67 PLAY               ;    Goto PLAY
    #                                                               ; ======================================================================   



def playMove():                     # PLMV: 0000000                 ; PLMV (playMove) procedure ============================================ 
    global a,b,d,threatCount        #
    global emptyIndex,cellIndex     #   
    global tupleIndex, moved        #
    global currentPlay              #   
    global advantageCount           #
    global moveType                 #
    #                                                               ; >> Reset THRT to -1 to keep track of whether there are two existing<<
    resetCounters()                 #       0 57 RCT                ;    link RCT (resetCounters)
    d = currentPlayPointer          #       0 30 _CP                ;    get  D <- _CP (currentPlayPointer)
    d = d + tupleLength             #       0 31 CTL                ;    add D + CTL (tupleLength)
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    tupleIndex = d                  #       0 34 VTX                ;    set D -> VTX (tupleIndex)
    #
    while True:                     #                               ; >>Set Starting PLAY CELL POINTER INDEX<<
        #                           # LMT1: 0 71 1                  ; LMT1: indirect address next instruction to D
        a = currentPlay[d]          #       0 10 0                  ;       get A <- Value @ D
        a = a + playsGridPointer    #       0 11 _PL                ;       add A + _PL (playGridPointer)
        d = a                       #       0 25 1                  ;       copy D -> A
        #                                   0 71 1                  ;       indirect address next instruction to D
        a = grid[d]                 #       0 10 0                  ;       get A <- value @ D 
        #
        #                                                           ;       >> If CELL value is 0 set update empty Index <<
        if a == 0:                  #       0 50 MT0                ;       if A = 0 GoTo MT0 (SubRoutine Call 0)
            updateEmptyIndex()      #                               ;       
        #
        #                                                           ;       >> If player cell increment computer threat count<<
        if a > 0:                   #       0 52 MT1                ;       if A > 0 goto MT1 (subroutince call 1)
            incrementThreatCount()  #                               ; 
        #
        #                                                           ;       >> If computer cell increment computer advantage count <<
        if a < 0:                   #       0 53 MT2                ;       if A IS NEGATIVE goto MT2 (subroutine call 2)
            incrementAdvCount()     #                               ; 
        #                                                           ;       Subroutine Links
        #                             MT0:  0 57 UEM                ;       MT0: link UEM (updateEmptyIndex)
        #                                   0 67 MTN1               ;            goto MTN1 (continue)
        #                             MT1:  0 57 ITC                ;       MT1: link  ITC (incrementThreatCount)
        #                                   0 67 MTN1               ;            goto MTN1 (continue)
        #                             MT2:  0 57 IAC                ;       MT2: link IAC (incrementAdv[antage]Count)
        #                                                           ;      
        #                                                           ;       >> Reset for next test
        d = tupleIndex              # MTN1: 0 30 VTX                ;       get D <- VTX (tupleIndex)
        d = d - const1              #       0 32 C1                 ;       subtract D - C1 (1) to Decrement PLAY CELL POINTER INDEX
        tupleIndex = d              #       0 34 VTX                ;       set D -> VTX (tupleIndex)  
        #
        #                                                           ;       >> Test if we've reached then end
        if d < 0: break             #       0 63 EMT1               ;       If D IS NEGATIVE goto EMT1 (break)
        else: pass                  #       0 67 LMT1               ;       goto LMT1  (loop repeat)
    #
    d = emptyIndex                  # EMT1: 0 30 VEX                ; EMT1: get D <- VEX (emptyIndex)                   Loop End
    if d < 0: return                #       0 63 PLMV               ;   if D (emptyIndex) IS NEGATIVE goto PLMV (return)   
    d = moveType                    #       0 30 MVT                ;   get D <- MVT (moveType)
    if d == 0: threatResponse()     #       0 60 MT3                ;   if D == 0 goto MT3 (link for threatResponse)
    elif d > 0: emptyMove()         #       0 62 MT6                ;   if D IS POSITIVE goto MT4 (link for emptyMove)
    else: advantageResponse()       #       0 57 ARS                ;   else gosub ARS (advantageREsponse)
    #                                                               ;        
    #                                                               ; >> links
    #                                 MT3:  0 57 TRS                ;    GoSub TRS (threatResponse)
    #                                       0 67 PLMV               ;    GoTo PLMV (return)
    #                                                               ; 
    #                                 MT6:  0 57 EMV                ;    GoSub EMV (make EmptyMove)
    return                          #       0 67 PLMV               ;    GoTo PLMV (return)
    #                                                               ; ====================================================================== 
                                                                
def threatResponse():               # TRS:  00000000                ; TRS (threatResponse) procedure =======================================
    d = threatCount                 #       0 30 VTC                ;   Get D <- VTX (threatCount)
    if d > 0:                       #       0 62 TR0                ;   If D (threatCount) > 0 then goto TR0
        makeCurrentMove()           #                               ;     
                                    #       0 67 TRS                ;   goto TRS (return)
                                    # TR0:  0 57 MCM                ;   link MCM (makeCurrentMove)
    else: return                    #       0 67 TRS                ;   goto TRS (return)
    #                                                               ; ====================================================================== 

def emptyMove():                    # EMV:  00000000                ; EMV (emptyMove) procedure ============================================
    d = emptyIndex                  #       0 30 VEX                ; get D <- VEX (emptyIndex)
    if d < 0: return                #       0 62 EMV                ;   if D IS POSITIVE goto EMV (return)
    makeCurrentMove()               #       0 57 MCM                ;   else link MCM (makeCurrentMove)
    #                                       0 67 EMV                ;   goto EMV (return)
    #                                                               ; ====================================================================== 

def advantageResponse():            # ARS:  00000000                ; ARS (advantageResponse) procedure ====================================
    d = advantageCount              # MT5:  0 30 VAC                ;  Get D <- VAC (advantageCount)  
    if d > 0:                       #       0 62 AR0                ;  If D (advantageCount) IS POSITIVEthen goto AR0
        makeCurrentMove()           #                               ;    Goto Subroutine MT4
        win()                       #                               ;
    else: return                    #       0 67 ARS                ; Goto ARS (return)
                                    # AR0:  0 57 MCM                ; GoSub MCM (makeCurrent Move)
                                    #       0 67 WIN                ; GoTo WIN
    #                                                               ; ====================================================================== 


def setCurrentPlay():               # SCPY: 0000000                 ; SCPY (setCurrentPlay) procedure ======================================
    global currentPlay              #                               ; > Copies the current play  (can probably refactor this out)
    global d, a, cellIndex          #
    global playsGridPointer         #                               ; >> Move current play pointer
    a = currentPlayPointer          #       0 10 _CP                ;    get A <- _CP (currentPlayPointer)
    a = a + tupleLength             #       0 11 CTL                ;    add A + CTL (tupleLength)
    a = a - const1                  #       0 12 C1                 ;    subtract A - C1 (1)
    d = playIndex                   #       0 30 VPX                ;    get D <- VPX (playIndex)
    cellIndex = d                   #       0 34 VCX                ;    set D -> VCX (cellIndex)
    #                                                               ;
    while True:                     #                               ; >> Copy the current play into a temporary array         
        #                             LFPL: 0 71 1                  ; LFPL: set address of next instruction to D     LOOP
        b = plays[d]                #       0 20 0                  ;       set B -> value @ D
        d = a                       #       0 25 1                  ;       copy A -> D  
        #                                   0 71 1                  ;       set address of next instruction to D                                 
        currentPlay[d] = b          #       0 24 0                  ;       set B -> _CP @ A offset
        a = a - const1              #       0 12 C1                 ;       subtract A - C1 (1)
        d = a                       #       0 25 1                  ;       copy A -> D
        d = d - currentPlayPointer  #       0 32 _CP                ;       subtract D - _CP
        if d < 0: return            #       0 63 SCPY               ;       if D IS NEGATIVE goto SCPY (return)        
        d = cellIndex               #       0 30 VCX                ;       get D <- VCX (cellIndex)
        d = d - const1              #       0 32 C1                 ;       subtract D - C1 (1) 
        cellIndex = d               #       0 34 VCX                ;       set D <- VCX (cellIndex)
        #                                   0 67 LFPL               ;       goto LFPL (Next Loop
    #                                                               ; ====================================================================== 


def initPlayScan():                 # IPS:  0000000                 ; IPS (initPlayScan) procedure ========================================= 
    global d, playLength            #                               ; >> Resets indexes to starting positions so we can scan again
    global playsGridPointer
    global playIndex                
    d = playsGridPointer            #       0 30 _PL                ;    Set D <- _PL (playGridPointer)
    d = d + playLength              #       0 31 CPL                ;    add D + CPL (playLength)
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    playIndex = d                   #       0 34 VPX                ;    set D -> VPLX (play Index)
    setCurrentPlay()                #       0 57 SCPY               ;    gosub SCPY (setCurrentPlay)
    return                          #       0 67 IPS                ;    goto IPS (return)    
    #                                                               ; ====================================================================== 


def resetCounters():                # RCT:  0000000                 ; RCT (resetCounters) procedure ========================================
    global d, const1, threatCount   #                               ; >> Sets threat, advantage and emptycell counterss to initial values -1
    global advantageCount           #
    global emptyIndex               #
    d = 0                           #       0 27 1                  ;    clear D      
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    threatCount = d                 #       0 34 VTC                ;    set D -> VTC (threatCount)
    advantageCount = d              #       0 34 VAC                ;    set D -> VAC (advantageCount)
    emptyIndex = d                  #       0 34 VEX                ;    set D -> VEX ([last]emptyIndex) 
    return                          #       0 67 RCT                ;    goto RCT (return)
    #                                                               ; ====================================================================== 


def makeCurrentMove():              # MCM:  0000000                 ; MCM (makeCurrentMove) procedure ======================================
    global a,d,emptyIndex           #                               ; >> Make the move currently indexed by VEX -- the index of the last 
    global grid, moved              #                               ; >> empty cell scanned
    global lastMove                 #                               ;
    a = 0                           #       0 27 0                  ;    clear A
    a = a - const1                  #       0 12 C1                 ;    subtract A - C1 (1)
    d = emptyIndex                  #       0 30 VEX                ;    get D <- VEX ([last]EmptyIndex]) 
    #                                       0 71 1                  ;    set address of next instruction to D 
    grid[d] = a                     #       0 14 0                  ;    set A -> value at D
    moved = a                       #       0 14 VM                 ;    set A -> VM (moved)  
    lastMove = d                    #       0 34 VLM                ;    set D -> VLM (lastMove)
    return                          #       0 67 MCM                ;    goto MCM (return)
    #                                                               ; ====================================================================== 


def updateEmptyIndex():             # UEM:  0000000                 ; UEM (updateEmptyIndex) procedure =====================================
    global emptyIndex,d             #                               ;
    emptyIndex = d                  #       0 34 VEX                ;    set D -> VEX (emptyIndex)
    return                          #       0 67 UEM                ;    gpto UEM (return)
    #                                                               ; ====================================================================== 


def incrementThreatCount():         # ITC:  0000000                 ; ITC (incrementThreatCount) procedure =================================
    global threatCount,a            #                               ;
    a = threatCount                 #       0 10 VTC                ;    set A <- VTC (threatCount)
    a = a + const1                  #       0 11 C1                 ;    sdd A + C1 (1)
    threatCount = a                 #       0 14 VTC                ;    set A -> VTC (threatCount)
    return                          #       0 67 ITC                ;    goto ITC (return)
    #                                                               ; ====================================================================== 

def incrementAdvCount():            # IAC:  0000000                 ; IAC (incrementAdvantageCount) procedure ==============================
    global advantageCount,a         #                               ;
    a = advantageCount              #       0 10 VAC                ;    Get A <- VAC (advantageCount)
    a = a + const1                  #       0 11 C1                 ;    Add A + C1 (1)
    advantageCount = a              #       0 14 VAC                ;    Set A -> VAC (advantageCount)
    return                          #       0 67 IAC                ;    Goto IAC (return)
    #                                                               ; ====================================================================== 


def win():                          # WIN:  0000000                 ; WIN procedure ========================================================
    global turn, switches           #                               ;
    showMove()                      #       0 57 SHMV               ;    link ShowMove  
    print("win")                    #                               ;
    #                               #       2 76 C1                 ;    Set IO to Addr C1 (1) input Switches and Stop
    input("Push Start: ")           #                               ;
    newGame()                       #       0 57 NEW                ;    link NEW [Game]
    playerFirstMove()               #       0 57 PFM                ;    link PFM (playerFirstMove)
    play()                          #       0 67 PLAY               ;    goto PLAY 
    #                                                               ; ====================================================================== 

def newGame():                      # NEW:  0000000                 ; NEW procedure ========================================================
    global moved, d, a, b, turn     #                               ;
    clearGrid()                     #       0 57 CGRD               ;    link CGRD (clearGrid)
    d = 0                           #       0 27 1                  ;    clear D
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 (1)
    moved = d                       #       0 34 VM                 ;    set D -> VM (moved)
    return                          #       0 67 NEW                ;    goto NEW (return)
    #                                                               ; ====================================================================== 

def clearGrid():                    # CGRD: 0000000                 ; CGRD (clearGrid) procedure ===========================================
    global a, d, constGridSize      #                               ;
    global gridPointer, playIndex   #                               ;
    global grid                     #                               ;
    d = gridPointer                 #       0 30 _PL                ;    get D <- _PL (gridPointer)
    d = d + constGridSize           #       0 31 CG                 ;    add D + CG (gridSize)
    while True:                     #                               ;
        d = d - const1              # LGR1: 0 32 C1                 ; LGR1: subtract D - C1 (1)                 LOOP
        a = d                       #       0 25 01                 ;       copy D -> A
        a = a - gridPointer         #       0 12 _PL                ;       subtract A - _PL (gridPointer)
        if a < 0:  return           #       0 53 CGRD               ;       if A IS NEGATIVE goto CRGD (return)
        #                           #       0 71 1                  ;       set address of next instruction to D                                         
        grid[d] = 0                 #       0 17 0                  ;       Clear memory location D      
        #                           #       0 67 LGR1               ;       goto LGR1 (next loop) 
    #                                                               ; ====================================================================== 




def playerFirstMove():              # PFM:  0000000                 ; PFM (playerFirstMove) proceedure =====================================
    global switches, turn, moved    #                               ;
    global d, a, grid, gridPointer  #                               ;
    d = switches                    #       0 04 1                  ;    get D <- IO-1
    d = d - const1                  #       0 32 C1                 ;    subtract D - C1 for 0 origin shift
    moved = d                       #       0 34 VM                 ;    set D -> VM (move) 
    d = d + gridPointer             #       0 31 _PL                ;    add D + _PL (gridPointer )
    a = 0                           #       0 27 0                  ;    clear A
    a = a + const1                  #       0 11 C1                 ;    add A + C1 (1)
    #                                       0 71 1                  ;    set address of next instruction to D 
    grid[d] = a                     #       0 14 0                  ;    set A -> value at D
    #
    #                                                               ; >> Set TURN to 1 -- indicates it's Computer turn next <<
    d = 0                           #       0 27 1                  ;    clear D 
    d = d - const1                  #       0 32 C1                 ;    substract D - C1 (1)                   
    turn = d                        #       0 34 VTN                ;    set D -> VTN (turn)    
    return                          #       0 67 PFM                ;    goto PFM (return)
    #                                                               ; ======================================================================


def showMove():                     # SHMV: 00000000                ; SHMV (showMove) proceuder ============================================
    str0 = None                     #       0 76 C2                 ; Set output to lamps
    if grid[0] == -1:
        str0 = "X"
    if grid[0] == 0:
        str0 = " "
    if grid[0] == 1:
        str0 = "O"
    str1 = None
    if grid[1] == -1:
        str1 = "X"
    if grid[1] == 0:
        str1 = " "
    if grid[1] == 1:
        str1 = "O"   
    str2 = None
    if grid[2] == -1:
        str2 = "X"
    if grid[2] == 0:
        str2 = " "
    if grid[2] == 1:
        str2 = "O"    
    str3 = None
    if grid[3] == -1:
        str3 = "X"
    if grid[3] == 0:
        str3 = " "
    if grid[3] == 1:
        str3 = "O"  
    str4 = None
    if grid[4] == -1:
        str4 = "X"
    if grid[4] == 0:
        str4 = " "
    if grid[4] == 1:
        str4 = "O"  
    str5 = None
    if grid[5] == -1:
        str5 = "X"
    if grid[5] == 0:
        str5 = " "
    if grid[5] == 1:
        str5 = "O"        
    str6 = None
    if grid[6] == -1:
        str6 = "X"
    if grid[6] == 0:
        str6 = " "
    if grid[6] == 1:
        str6 = "O" 
    str7 = None
    if grid[7] == -1:
        str7 = "X"
    if grid[7] == 0:
        str7 = " "
    if grid[7] == 1:
        str7 = "O"   
    str8 = None
    if grid[8] == -1:
        str8 = "X"
    if grid[8] == 0:
        str8 = " "
    if grid[8] == 1:
        str8 = "O"   
    print ( str0 + "|" + 
        str1 + "|" + str2)
    print ("-----")
    print ( str3 + "|" + 
        str4 + "|" + str5)
    print ("-----")
    print ( str6 + "|" + 
        str7 + "|" + str8)          #                               ; >> Output move to Lamps and stop <<
    d= lastMove                     #       0 30 VLM                ;    Get D <- VLM(lastMove)
    d = d + const1                  #       0 31 C1                 ;    Add D + C1 (1) offset zero + 1
    print(d)                        #       2 05 1                  ;    STOP Output D ->
    return                          #       0 67 SHMV               ;    goto SHMV (return)
    #                                                               ; ====================================================================== 


    
 
if __name__ == "__main__":          #                           ;
   main(sys.argv[1:])               #                           ;