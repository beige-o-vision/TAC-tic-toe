#TAC-tic-toe

TAC-tic-toe is a noughts and crosses game.  The players are the computer operator and the computer itself. The operator (you!) win by placing three of your moves in a line within the grid. These may be in a horizontal, vertical or diagnal line. Players take turns placing their marks. You make either offensive moves to complete your line, or defensive, to block a line built by the computer.

Moves are indicated using the switches and lamps of the computer console. The computer will display its move as a binary number representing a grid location in the lamps. You will tell the computer your move by placing the grid location on the switches, then pressing the start switch. 

The game uses the following grid.

| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

In the following example. The winning player (X) has played grid-cell 1, 5 & 9.

| X |   | O |
| O | X |   |
| O |   | X |


##Operating Instructions

1. Load the tape 
2. Load the start address of the tape
3. To play first, enter your move on the switches
4. For the computer to play first, clear the switches
5. Press the 'Start' switch
6. The digits in the display will indicate the computer's move
7. Enter your move on the switches
8. Press the 'Start' switch
9. If you last move was disallowed, the computer will display an empty display (0). This indicates you need to re-enter you move from step 7.
10. Otherwise the computer will display its next move.
11. Repeat steps 7-10 until a game outcome is indicated. 

##Game outcomes
- **DRAW:** Alternating digits on the screen indicate a draw (eg. 1010 -> 0101 -> 1010 -> ...)
- **COMPUTER WINS:** All digits flashing indicates the computer has won (eg. 1111 -> 0000 -> 1111 -> ...)
- **YOU WIN:** One digit scrolling indicates you have won (eg. 0001 -> 0010 -> 0100 -> ...)

To play again, wait for the display and computer to stop. Clear the switches, press start.  The computer will play first.

##Theory of Operation
The program completes a 'perfect' game of nought and crosses. It's therefore only plossible to draw with the computer, or for the computer to win. Only these options exist in the code.
Game state is represented by a nine-word array. Each cell in the grid gets its own word.  The grid is numbered left-to-right in rows from top-to-bottom.  Players provide the number of their cell to play that cell. 
The words hold one of three values. A 0 indicates the cell hasn't been played. The computer marks its cells with a -1.  The player's cells are marked with a 1. 
There are computer stores a representation of all potential winning patterns.  The are stored as the coordinates of only the winning cells. Each winning pattern is a three word array.  The words contain the 0 origin address of the grid cell.  Therefore cell 1 is actually stored as cell 0. All the possible wins are stored in a continuous list.  There are 8 possible winning moves of 3 moves each -- resulting in a 24 word array.
To determine whether there's a winning game, the computer reads each play, and tests the grid to determin if it has won using that play.  The computer doesn't test the player's moves.  This isn't necessary as it's impossible for the player to win. The computer runs a test to see if it's won after every move.
To determine whether there's a drawn game, the computer first determines whether there has been a win.  Then the computer scans the game grid to see if there are any unplayed cells. These are represented by the value 0. If there are no 0s left, and no wins, it determines the game is drawn. The computer runs this test after testing for a win, if the win test is false.  It will therefore run this test ever move it makes, except for a winning move.
The player's move is requested when the computer displays its move and stops the machine. The move is entered on switches.  When the player restart the machine, the computer immediate reads the move. It checks the grid to make sure the cell is actually free to play.  If it isn't the computer halts again.  This allows the player to make another move -- again by entering the move and starting the computer. It will not proceed to the next move until the player offers a valid move.
Once a valid move is detected, the computer stores a 1 in the grid.  It then plays its own move.
The computer makes its move by evaluating threat and advantage. If there's no threat to defend or advantage to use, it will play the first available cell in the grid -- starting from the bottom right. To evaluate threat, the computer using its winning plays list. For each potential winning play, it counts the current moves by each player. If there are two moves by the player it is considered a threat. If there are two existing moves by the computer it considers it an advantage.  While scanning it also keeps trac of the last available cell in the potential play. If there's no available cell the computer moves onto the next play in the play list. Otherwise if there's either an advantage or threat, the computer makes the available play. It then stops evaluating the grid and displays its move. 
If the computer completes a scan of the grid and finds no advantage or threat, it begins scanning again. It goes potential play, by potential play. It will make the first available move.
The computer signals its move by writing it in binary form to the display lamps on the console. It then stops, until the player starts the machine after their move.
Outcome display is made for a computer win or game draw.  This is a looped pattern on the display. The player win isn't implemented as this is impossible. Once the display stops animating, the computer is read to play again. It indicates this by displaying the first move of a new game, then stopping.

