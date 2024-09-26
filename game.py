import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 300, 300
cell_size = 10

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # User Snake Color
BLUE = (0, 0, 255)   # AI Snake Color
RED = (255, 0, 0)

# Set up the display
window = pygame.display.set_mode((width, height * 2))  # Double the height for user and AI snakes
pygame.display.set_caption("Reinforcement Learning Snake Game")

clock = pygame.time.Clock()

# Define Snake class
class SnakeGame:
    def __init__(self, color):
        self.snake = [(width // 2 // cell_size, height // 2 // cell_size)]
        self.direction = (1, 0)
        self.food = self.place_food()
        self.score = 0
        self.done = False
        self.color = color  # Color for each snake (either GREEN for user or BLUE for AI)

    def place_food(self):
        return (random.randint(0, (width // cell_size) - 1), random.randint(0, (height // cell_size) - 1))

    def step(self, action):
        if action == 0:  # up
            self.direction = (0, -1)
        elif action == 1:  # down
            self.direction = (0, 1)
        elif action == 2:  # left
            self.direction = (-1, 0)
        elif action == 3:  # right
            self.direction = (1, 0)

        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Check if snake hits the wall or itself
        if head[0] < 0 or head[0] >= width // cell_size or head[1] < 0 or head[1] >= height // cell_size or head in self.snake:
            self.done = True
            return -10

        self.snake.insert(0, head)

        # Check if food is eaten
        if head == self.food:
            self.score += 1
            self.food = self.place_food()
            return 10
        else:
            self.snake.pop()

        return 0

    def reset(self):
        self.snake = [(width // 2 // cell_size, height // 2 // cell_size)]
        self.direction = (1, 0)
        self.food = self.place_food()
        self.score = 0
        self.done = False

    def render(self, surface, offset):
        for block in self.snake:
            pygame.draw.rect(surface, self.color, (block[0] * cell_size, block[1] * cell_size + offset, cell_size, cell_size))
        pygame.draw.rect(surface, RED, (self.food[0] * cell_size, self.food[1] * cell_size + offset, cell_size, cell_size))

# Improved AI with basic logic to move towards the food
class SimpleAI:
    def choose_action(self, snake_game):
        head = snake_game.snake[0]
        food = snake_game.food

        # Simple AI logic to move towards the food
        if head[0] < food[0]:  # Move right
            return 3
        elif head[0] > food[0]:  # Move left
            return 2
        elif head[1] < food[1]:  # Move down
            return 1
        elif head[1] > food[1]:  # Move up
            return 0

        # Default random action if aligned with food
        return random.randint(0, 3)

# Main game loop
def main():
    user_game = SnakeGame(GREEN)  # User snake is green
    ai_game = SnakeGame(BLUE)     # AI snake is blue
    ai_agent = SimpleAI()
    
    user_score = 0
    ai_score = 0
    users_played = 0
    user_wins = 0
    
    font = pygame.font.SysFont("Arial", 20)

    running = True
    while running:
        window.fill(BLACK)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # AI game logic
        if not ai_game.done:
            ai_action = ai_agent.choose_action(ai_game)
            ai_game.step(ai_action)
        else:
            ai_game.reset()  # Reset AI game if it finishes
        ai_game.render(window, 0)  # Render AI snake on the top half (offset = 0)

        # User controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            user_game.step(0)
        elif keys[pygame.K_DOWN]:
            user_game.step(1)
        elif keys[pygame.K_LEFT]:
            user_game.step(2)
        elif keys[pygame.K_RIGHT]:
            user_game.step(3)

        if user_game.done:
            users_played += 1
            if user_game.score > ai_game.score:
                user_wins += 1
            user_game.reset()

        user_game.render(window, height)  # Render user snake on the bottom half (offset = height)
        
        # Display scores and statistics
        score_text = font.render(f"AI Score: {ai_game.score}", True, WHITE)
        window.blit(score_text, (10, 10))
        user_score_text = font.render(f"User Score: {user_game.score}", True, WHITE)
        window.blit(user_score_text, (10, height + 10))

        stats_text = font.render(f"Users Played: {users_played}, User Wins: {user_wins}", True, WHITE)
        window.blit(stats_text, (10, height + 30))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
