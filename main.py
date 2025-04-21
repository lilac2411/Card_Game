##
# PointClickCare Early Tech Talent Incubator Program
# 21 Card Game Coding Challenge
##

# Setup Pygame
import random
import pygame
pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PointClickCare Coding Challenge")

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

## MODEL - Data use in system

# Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 222, 90)
RED = (225, 56, 33)
PINK = (246, 201, 180)

dealersTurn = False
playerLost = False
playerWon = False
tie = False
gameOver = False
soundPlayed = False
titlePage = True
playerWins = 0
dealerWins = 0
outcome = 0
playerHand = []
dealerHand = []

font = pygame.font.SysFont('Calibri', 30, True, False)

# Images created by me in Canva!
sideBar = pygame.image.load("assets/sideBar.png").convert()
titleImg = pygame.image.load("assets/title.png").convert()

# Image found on Canva from "Deena Rutter Team"
background = pygame.image.load("assets/woodBackground.png").convert()

# Sound effects from https://pixabay.com/ 
winSound = pygame.mixer.Sound("assets/winSound.ogg")
lossSound = pygame.mixer.Sound("assets/lossSound.ogg")

# Make sound effects quieter
winSound.set_volume(0.4)
lossSound.set_volume(0.3)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = 0
        self.dealersHand = False
        self.colour = BLACK # colour will change later on based on suit
        self.xPos = 100
        self.yPos = 0
        self.size = [100,160]
        
    def draw(self, surface):

        # Card goes at the top of the screen if it's the dealer's card
        if self.dealersHand:
            self.yPos = 20
            
        # Card goes at the bottom of screen if it is the player's
        else:
            self.yPos = 600-self.size[1]-20
        
        # Draw the card and its border
        pygame.draw.rect(surface, self.colour, [self.xPos, self.yPos,
                                                self.size[0],self.size[1]])
        pygame.draw.rect(surface, WHITE, [self.xPos+4, self.yPos+4, 
                                          self.size[0]-8,self.size[1]-8])
        
        # Display the card's rank
        text = self.rank
        display = font.render(text, True, self.colour)
        surface.blit(display, [self.xPos+20, self.yPos+20])
        
        # Display the card's suit
        if self.suit == "H":
            self.colour = RED
            text = "♥"
        elif self.suit == "S":
            text = "♠"
        elif self.suit == "C":
            text = "♣"
        elif self.suit == "D":
            text = "♦"
            self.colour = RED
            
        display = font.render(text, True, self.colour)
        surface.blit(display, [self.xPos+20, self.yPos+45])
    
    # Dealer's first card is face down
    def drawFaceDown(self, surface):
        self.yPos = 20
        pygame.draw.rect(surface, BLACK, [self.xPos, self.yPos, 
                                          self.size[0],self.size[1]])

# Setting up a deck of 52
def setupDeck():
    
    deck = []
    suits = ["D", "S", "H", "C"] 
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    # Generating all cards based on the suits and ranks
    for suit in suits:
        for rank in ranks:
            deck.append(Card(rank, suit))

    return deck

# Adding cards to player/dealer's hand
def dealCard(hand):
    card = random.choice(cardDeck)
    
    # Identify if card is the dealer's (so it can be drawn in the right spot)
    if hand is dealerHand:
        card.dealersHand = True
        
    hand.append(card)
    cardDeck.remove(card)

# Getting the total value of one's hand
def cardTotal(hand):
    totalValue = 0

    # Add the value of each card to get the hand's total
    for card in hand:
        
        # Jacks, queens, and kings are worth 10
        if card.rank in ["J", "Q", "K"]:
            card.value = 10
        
        # Aces count as either 11 or 1 (if 11 would bust the hand)
        elif card.rank == "A":
            if totalValue + 11 > 21:
                card.value = 1
            else:
                card.value = 11
        else:
            card.value = int(card.rank)

        totalValue += card.value
    
    return totalValue

# Display who won when round is over
def printResults(outcome, surface):
    
    if outcome == 1:
        text = "BUST!!! You lost :("
    elif outcome == 2:
        text = "DEALER BUST! You won!"
    elif outcome == 3:
        text = "YOU WON!!!! Congrats :)"
    elif outcome == 4:
        text = "YOU LOST. Better luck next time!"
    elif outcome == 5:
        text = "You tied!"
    elif outcome == 6:
        text = "21! You win :)"

    display = font.render(text, True, BLACK)
    surface.blit(display, [100, 250])

# Show hand totals
def scoreBoard(surface):
    screen.blit(sideBar, [590,0])
    font = pygame.font.SysFont('Calibri', 22, True, False)
    display = font.render("Your total: " + str(cardTotal(playerHand)), 
                          True, YELLOW)
    surface.blit(display, [610, 450])
    
    # Only show dealer's total when all their cards are revealed
    if dealersTurn:
        display = font.render("Dealer's total: "  + str(cardTotal(dealerHand)),
                              True, RED)
        surface.blit(display, [610, 490])

cardDeck = setupDeck()

# Both player + dealer get 2 cards to start with
for i in range(2):
    dealCard(playerHand)
    dealCard(dealerHand)

## Main Program Loop
while not done:
    ## CONTROL
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        # When on the title page, user can only press space
        elif titlePage:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                titlePage = False
        
        # Only allow player to hit or stay if game isn't over
        elif event.type == pygame.KEYDOWN and not gameOver:
            
            # Player decides to 'HIT', deal a card
            if event.key == pygame.K_h:
                dealCard(playerHand)
            
            # Player decides to 'STAY'
            elif event.key == pygame.K_s:
                dealersTurn = True
                
                # Dealer is dealt cards until their total is 16 or over
                while cardTotal(dealerHand) < 16:
                    dealCard(dealerHand)
        
        # Only allow player to start a new round when game is over
        elif event.type == pygame.MOUSEBUTTONDOWN and gameOver:
            
            # Player starts a new round by clicking the button:
            if button_rect.collidepoint(event.pos):
                
                # Update win/loss scoreboard
                if playerWon:
                    playerWins +=1
                elif playerLost:
                    dealerWins +=1
                soundPlayed = False
                
                # Reset everything for new round
                playerHand.clear()
                dealerHand.clear()
                cardDeck = setupDeck()
                dealersTurn = False
                playerLost = False
                playerWon = False
                tie = False
                gameOver = False
                
                # Deal 2 new cards each
                for i in range(2):
                    dealCard(playerHand)
                    dealCard(dealerHand)
                
    # Game logic
    
    # Find who won based on total of hand
    if cardTotal(playerHand) > 21:
        playerLost = True # Player busts
        outcome = 1
    elif cardTotal(dealerHand) > 21:
        playerWon = True # Dealer busts
        outcome = 2
    elif cardTotal(playerHand) == 21:
        playerWon = True
        outcome = 6
    elif dealersTurn:
        
        # At this point, both hands aren't greater than 21
        # Whoever has the higher hand wins
        if cardTotal(playerHand) > cardTotal(dealerHand):
            playerWon = True
            outcome = 3
        elif cardTotal(playerHand) < cardTotal(dealerHand):
            playerLost = True
            outcome = 4
        else:
            tie = True
            outcome = 5
    
    # Once an outcome is reached, print results on screen
    if playerWon or playerLost or tie:
        gameOver = True
    
    ## VIEW
    # Clear screen
    screen.fill(WHITE)
    
    # Draw
    if titlePage:
        screen.blit(titleImg, [0,0])
    else:
        screen.blit(background, [0,0])        
        
        # Dealer's 1st card is face down to begin with
        if not dealersTurn:
            dealerHand[0].xPos = 100
            dealerHand[0].drawFaceDown(screen)
        else: # If it's the dealer's turn, reveal 1st card
            dealerHand[0].draw(screen)
        
        # Displaying the dealer's cards on the table
        for i, card in enumerate(dealerHand[1:]):
            card.xPos = 100 + (i + 1) * 80
            card.draw(screen)
        
        # Displaying the player's cards on the table
        for i, card in enumerate(playerHand):
            card.xPos = 100 + i * 80 
            card.draw(screen)
        
        # Display hand totals for player and dealer
        scoreBoard(screen)
        
        # Add labels for each hand and a round win/loss counter
        text = font.render(("DEALER"), True, WHITE)
        screen.blit(text, (100, 180))
        
        text = font.render(("PLAYER"), True, WHITE)
        screen.blit(text, (100, 385))
        
        text = font.render(("WINS"), True, WHITE)
        screen.blit(text, (640, 100))

        text = font.render("Player: " + str(playerWins), True, YELLOW)
        screen.blit(text, (630, 150))
        
        text = font.render("Dealer: " + str(dealerWins), True, RED)
        screen.blit(text, (630, 200))
        
        text = font.render(("[H]it"), True, PINK)
        screen.blit(text, (640, 300))
        
        text = font.render(("[S]tay"), True, PINK)
        screen.blit(text, (640, 350))
        
        # Play a sound effect when player wins/loses
        if not soundPlayed:
            if playerWon:
                winSound.play()
                soundPlayed = True
            elif playerLost:
                lossSound.play()
                soundPlayed = True
        
        # Ask them if they want to play again
        if gameOver:
            printResults(outcome, screen)
            button_rect = pygame.Rect(200, 300, 210, 50)
            pygame.draw.rect(screen, BLACK, button_rect)
            text = font.render("Play Again?", True, PINK)
            screen.blit(text, (button_rect.x + 20, button_rect.y + 5))
    
    # Update Screen
    pygame.display.flip()
    clock.tick(60)

# Close the window and quit
pygame.quit()