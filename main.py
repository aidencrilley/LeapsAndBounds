import arcade


# Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
MOVEMENT_SPEED = 5
BACKGROUND_COLOR = arcade.color.GRAY
GAME_TITLE = "Doggo Simulator"
GAME_SPEED = 1/60

class Window(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.dog_list = None
        self.dog_sprite = None

    def setup(self):
        """ Setup the game (or reset the game) """
        arcade.set_background_color(BACKGROUND_COLOR)
        self.dog_list = arcade.SpriteList()
        self.dog_sprite = Dog("images/dog.png", scale = 2)
        self.dog_list.append(self.dog_sprite)

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        self.dog_list.draw()

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.dog_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.dog_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.dog_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.dog_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.dog_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

class Dog(arcade.Sprite):
    timer: int

    #def __init__(self):
        #super().__init__()
        #self.texture = dog_sprite
        #self.center_x = WINDOW_WIDTH/2
        #self.center_y = WINDOW_HEIGHT/2

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