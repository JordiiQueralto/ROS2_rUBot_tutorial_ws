#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class MoveTurtle(Node):
    def __init__(self):
        super().__init__('move_turtle')

        # Publicador al tópico /turtle1/cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Suscriptor al tópico /turtle1/pose
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10)
        self.subscription  # evitar warning de variable no usada

        self.get_logger().info('Nodo /move_turtle inicializado.')

    def pose_callback(self, msg):
        twist = Twist()

        # Si el robot se pasa de los límites, se detiene
        if msg.x > 7.0 or msg.y > 7.0:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().info(f"Tortuga fuera de límites: x={msg.x:.2f}, y={msg.y:.2f}. Deteniendo.")
        else:
            twist.linear.x = 1.0   # Velocidad constante hacia adelante
            twist.angular.z = 0.5  # Giro constante

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
