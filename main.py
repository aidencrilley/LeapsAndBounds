import arcade

# Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLUE_GRAY
GAME_TITLE = "Doggo Simulator"
GAME_SPEED = 1/60

MOVEMENT_SPEED = 4
GRAVITY = 5
JUMP_SPEED = 4.5


class Window(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)

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

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.dog_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.dog_sprite = Dog("images/dog.png", scale=2)
        self.dog_list.append(self.dog_sprite)

        # Creating the ground
        for x in range(0, 1250, 800):
            wall = arcade.Sprite("images/grass.png")
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.dog_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()

        self.dog_list.draw()
        self.wall_list.draw()

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


class Dog(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH - 1:
            self.right = WINDOW_WIDTH - 1

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