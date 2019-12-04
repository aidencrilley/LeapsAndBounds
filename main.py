import random

import arcade

# Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLUE_GRAY
GAME_TITLE = "Doggo Simulator"
GAME_SPEED = 1 / 60

# Game states

INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

SPRITE_SCALING = 0.5
TILE_SCALING = 0.1

MOVEMENT_SPEED = 4
GRAVITY = 5
JUMP_SPEED = 6

LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class Window(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)

        self.current_state = INSTRUCTIONS_PAGE_0

        # Sprite Lists
        self.dog_sprite = None
        self.dog_list = None
        self.wall_list = None

        # Setting up the player
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        # set up score
        self.score = 0

        self.instructions = []
        texture = arcade.load_texture("images/instructions_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instructions_1.png")
        self.instructions.append(texture)

    def setup(self):
        """ Setup the game (or reset the game) """

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        arcade.set_background_color(BACKGROUND_COLOR)
        self.dog_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.dog_sprite = Dog("images/dog.png", scale=2)
        self.dog_sprite.center_x = 64
        self.dog_list.append(self.dog_sprite)

        # Creating the ground
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/grass.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[256, random.randint(150, 450)],
                           [356, random.randint(150, 450)],
                           [456, random.randint(150, 450)],
                           [556, random.randint(150, 450)],
                           [656, random.randint(150, 450)],
                           [756, random.randint(150, 450)]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite("images/RTS_Crate.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.dog_sprite, self.wall_list, GRAVITY)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

    def draw_game(self):
        self.dog_list.draw()
        self.wall_list.draw()

    def on_draw(self):
        """ Called when it is time to draw the world """
        self.dog_list.draw()
        self.wall_list.draw()

        arcade.start_render()

        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.dog_sprite.change_x = 0
        self.dog_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.dog_sprite.change_y = JUMP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.dog_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.dog_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.dog_sprite.change_x = MOVEMENT_SPEED

        self.dog_list.update()
        self.physics_engine.update()

     #   wall_hit_list = arcade.check_for_collision_with_list(self.dog_list, self.wall_list)

       # for wall in wall_hit_list:
        #    self.score += 1

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.dog_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.dog_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WINDOW_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.dog_sprite.right > right_boundary:
            self.view_left += self.dog_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + WINDOW_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.dog_sprite.top > top_boundary:
            self.view_bottom += self.dog_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.dog_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.dog_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                WINDOW_WIDTH + self.view_left,
                                self.view_bottom,
                                WINDOW_HEIGHT + self.view_bottom)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.up_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def on_mouse_press(self, x, y, button, modifiers):
    if self.current_state == INSTRUCTIONS_PAGE_0:
        self.current_state = INSTRUCTIONS_PAGE_1
    elif self.current_state == INSTRUCTIONS_PAGE_1:
        self.setup()
        self.current_state = GAME_RUNNING
    elif self.current_state == GAME_OVER:
        self.setup()
        self.current_state = GAME_RUNNING


def update(self, delta_time):
    if self.current_state == GAME_RUNNING:
        self.dog_list.update()

        hit_list = arcade.check_for_collision_with_list(self.dog_sprite, self.wall_list)

    for wall in self.wall_list:

        if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
            wall.change_x *= -1
        if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
            wall.change_x *= -1
        if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
            wall.change_y *= -1
        if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
            wall.change_y *= -1


class Dog(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1


def main():
    window = Window()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
