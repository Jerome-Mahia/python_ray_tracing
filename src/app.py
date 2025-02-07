# Import necessary modules and classes
from config import *
import engine
import scene


class App:
    """
    Represents the main application that controls high-level functions such as handling input and rendering scenes.
    """

    def __init__(self):
        """
        Initialize the App object, setting up GLFW, creating assets, configuring input systems, and starting the main loop.
        """

        self.screenWidth = 1500
        self.screenHeight = 1000

        # Set up GLFW
        self.set_up_glfw()

        # Create assets and graphics engine
        self.make_assets()

        # Set up input systems
        self.set_up_input_systems()

        # Set up framerate timer
        self.set_up_timer()

        # Run the main loop
        self.mainLoop()

    def set_up_glfw(self) -> None:
        """
        Set up GLFW with specific configuration.
        """

        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, False)
        self.window = glfw.create_window(self.screenWidth, self.screenHeight, "Title", None, None)
        glfw.make_context_current(self.window)

    def make_assets(self) -> None:
        """
        Create necessary assets for the program, including the graphics engine and scene.
        """

        self.graphicsEngine = engine.Engine(self.screenWidth, self.screenHeight)
        self.scene = scene.Scene()

    def set_up_input_systems(self) -> None:
        """
        Configure the mouse and keyboard input systems.
        """

        glfw.set_input_mode(self.window, GLFW_CONSTANTS.GLFW_CURSOR, GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN)
        glfw.set_cursor_pos(self.window, self.screenWidth // 2, self.screenHeight // 2)

        self.walk_offset_lookup = {
            1: 0,
            2: 90,
            3: 45,
            4: 180,
            6: 135,
            7: 90,
            8: 270,
            9: 315,
            11: 0,
            12: 225,
            13: 270,
            14: 180
        }

    def set_up_timer(self) -> None:
        """
        Set up the framerate timer.
        """

        self.lastTime = glfw.get_time()
        self.currentTime = glfw.get_time()
        self.numFrames = 0
        self.frameTime = 0
        self.lightCount = 0

    def mainLoop(self) -> None:
        """
        Run the main program loop, handling events, rendering, and updating timing.
        """

        running = True
        while running:
            # Handle events
            if glfw.window_should_close(self.window) or glfw.get_key(self.window,
                                                                     GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                running = False

            self.handleKeys()
            self.handleMouse()

            glfw.poll_events()

            # Render
            self.graphicsEngine.renderScene(self.scene)

            # Timing
            self.calculateFramerate()
        self.quit()

    def handleKeys(self) -> None:
        """
        Handle the current key state, updating the player's position.
        """

        rate = self.frameTime / 16
        combo = 0

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 1
        elif glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 2
        elif glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 4
        elif glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            combo += 8

        if combo in self.walk_offset_lookup:
            angle = np.radians(self.walk_offset_lookup[combo])
            dx = 0.1 * rate * np.cos(angle)
            dy = -0.1 * rate * np.sin(angle)
            self.scene.move_player(dx, dy)

    def handleMouse(self) -> None:
        """
        Handle mouse movement, updating the player's direction.
        """

        (x, y) = glfw.get_cursor_pos(self.window)
        rate = self.frameTime / 16.667
        theta_increment = rate * ((self.screenWidth / 2.0) - x)
        phi_increment = rate * ((self.screenHeight / 2.0) - y)

        self.scene.spin_player([theta_increment, phi_increment])
        glfw.set_cursor_pos(self.window, self.screenWidth // 2, self.screenHeight // 2)

    def calculateFramerate(self) -> None:
        """
        Calculate the framerate of the program and update the window title.
        """

        self.currentTime = glfw.get_time()
        delta = self.currentTime - self.lastTime
        if delta >= 1:
            framerate = int(self.numFrames / delta)
            glfw.set_window_title(self.window, f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = float(1000.0 / max(60, framerate))
            self.graphicsEngine.adaptResolution(framerate)
        self.numFrames += 1

    def quit(self) -> None:
        """
        Terminate the program, cleaning up resources.
        """

        # self.graphicsEngine.destroy()
        glfw.terminate()
