import cv2
import numpy as np
import time

class Ball:
    def __init__(self, x, y, radius=20, color=(255, 0, 0)):
        """
        Initialize the Ball object.
        
        :param x: Initial x-coordinate of the ball
        :param y: Initial y-coordinate of the ball
        :param radius: Radius of the ball
        :param color: Color of the ball in BGR format
        """
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.color = color
        self.velocity = np.array([0.0, 0.0], dtype=np.float64)
        self.gravity = 0.5 # TODO: Modify rates later for more realistic effects
        self.bounce_factor = 0.8
        self.trampoline_boost = 15
        self.last_collision_time = 0
        self.collision_cooldown = 0.5 # 0.5 second cooldown for stuttering

    def move(self):
        """
        Update the ball's position based on its velocity and apply gravity.
        """
        self.velocity[1] += self.gravity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def bounce_trampoline(self, line_angle):
        """
        Apply a trampoline bounce effect to the ball.
        
        :param line_angle: Angle of the trampoline line
        :return: True if bounce occurred, False otherwise
        """
        current_time = time.time()
        if current_time - self.last_collision_time > self.collision_cooldown:
            # Calc bounce direction based on trampoline line angle
            # Bounce direction is perpendicular to line
            bounce_direction = np.array([np.sin(line_angle), -np.cos(line_angle)])

            # Apply trampoline boost
            self.velocity = bounce_direction * self.trampoline_boost
            self.last_collision_time = current_time
            return True
        return False

    def draw(self, frame):
        """
        Draw the ball on the given frame.
        
        :param frame: The frame to draw the ball on
        """
        cv2.circle(frame, (int(self.x), int(self.y)), self.radius, self.color, -1)

    def check_boundary(self, width, height):
        """
        Check and handle collisions with screen boundaries.
        
        :param width: Width of the screen
        :param height: Height of the screen
        """
        # left and right boundaries collision
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.velocity[0] *= -self.bounce_factor
            self.x = np.clip(self.x, self.radius, width - self.radius)
        
        # top boundary collision
        if self.y - self.radius <= 0:
            self.velocity[1] *= -self.bounce_factor
            self.y = self.radius

        # bottom boundary collision ---> TODO: change to end game later on
        elif self.y + self.radius >= height:
            self.velocity[1] *= -self.bounce_factor
            self.y = height - self.radius

    def check_trampoline_collision(self, p1, p2):
        """
        Check if the ball collides with the trampoline line and apply bounce if it does.
        
        :param p1: First point of the trampoline line
        :param p2: Second point of the trampoline line
        :return: True if collision occurred, False otherwise
        """
        # Calc vector of trampoline line
        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1]], dtype=np.float64)
        # Calc veactor from first point to ball center
        v2 = np.array([self.x - p1[0], self.y - p1[1]], dtype=np.float64)
        
        # Calc scalar proj of v2 onto v1
        projection = np.dot(v2, v1) / np.dot(v1, v1)

        # check if proj point is on line segment
        if 0 <= projection <= 1:
            # find closest point on line to ball center and calc distance
            closest_point = np.array(p1, dtype=np.float64) + projection * v1
            distance = np.linalg.norm(np.array([self.x, self.y]) - closest_point)
            
            # if distance <= ball radius, calc angle of trampoline and apply bounce
            if distance <= self.radius:
                line_angle = np.arctan2(v1[1], v1[0])
                return self.bounce_trampoline(line_angle)
        return False

    def get_collision_cooldown_status(self):
        """
        Check if the ball is currently in a collision cooldown period.
        
        :return: True if in cooldown, False otherwise
        """
        return time.time() - self.last_collision_time <= self.collision_cooldown





