#!/usr/bin/env python3
"""
Terminal Diwali Fireworks Celebration
A beautiful ASCII fireworks display in your terminal!
"""

import sys
import time
import random
import math
from collections import deque

# Check if running on Windows
IS_WINDOWS = sys.platform.startswith('win')

if IS_WINDOWS:
    import os
    os.system('color')

# ANSI Color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Regular colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;213m'
    PURPLE = '\033[38;5;141m'
    GOLD = '\033[38;5;220m'
    
    # Bright colors
    BRIGHT_RED = '\033[38;5;196m'
    BRIGHT_GREEN = '\033[38;5;46m'
    BRIGHT_YELLOW = '\033[38;5;226m'
    BRIGHT_BLUE = '\033[38;5;51m'
    BRIGHT_MAGENTA = '\033[38;5;201m'
    
    @staticmethod
    def random_color():
        colors = [
            Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE,
            Colors.MAGENTA, Colors.CYAN, Colors.ORANGE, Colors.PINK,
            Colors.PURPLE, Colors.GOLD, Colors.BRIGHT_RED, Colors.BRIGHT_GREEN,
            Colors.BRIGHT_YELLOW, Colors.BRIGHT_BLUE, Colors.BRIGHT_MAGENTA
        ]
        return random.choice(colors)

class Particle:
    def __init__(self, x, y, vx, vy, color, char='*'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.char = char
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.trail = deque(maxlen=3)
    
    def update(self):
        self.trail.append((int(self.x), int(self.y)))
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.15  # Gravity
        self.vx *= 0.98  # Air resistance
        self.life -= 1
        return self.life > 0

class Rocket:
    def __init__(self, x, target_y, color):
        self.x = x
        self.y = 0
        self.target_y = target_y
        self.color = color
        self.vy = -2.0
        self.exploded = False
        self.trail = deque(maxlen=5)
    
    def update(self):
        self.trail.append((int(self.x), int(self.y)))
        self.y += self.vy
        self.vy += 0.05
        
        if self.y >= self.target_y:
            self.exploded = True
            return True
        return False

class Firework:
    def __init__(self, x, y, firework_type='burst'):
        self.x = x
        self.y = y
        self.particles = []
        self.type = firework_type
        self.color = Colors.random_color()
        self.create_particles()
    
    def create_particles(self):
        if self.type == 'burst':
            particle_count = random.randint(30, 50)
            for _ in range(particle_count):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.5, 2.0)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                char = random.choice(['*', '·', '•', '+', '✦', '✧'])
                self.particles.append(Particle(self.x, self.y, vx, vy, self.color, char))
        
        elif self.type == 'ring':
            particle_count = 40
            for i in range(particle_count):
                angle = (2 * math.pi * i) / particle_count
                speed = 1.5
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append(Particle(self.x, self.y, vx, vy, self.color, '○'))
        
        elif self.type == 'willow':
            particle_count = random.randint(40, 60)
            for _ in range(particle_count):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.3, 1.0)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed - 1.5
                self.particles.append(Particle(self.x, self.y, vx, vy, self.color, '|'))
        
        elif self.type == 'heart':
            particle_count = 30
            for i in range(particle_count):
                t = (i / particle_count) * 2 * math.pi
                x_offset = 16 * math.sin(t) ** 3
                y_offset = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
                vx = x_offset * 0.08
                vy = y_offset * 0.08
                self.particles.append(Particle(self.x, self.y, vx, vy, Colors.PINK, '♥'))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0

class Terminal:
    def __init__(self, width=100, height=30):
        self.width = width
        self.height = height
        self.buffer = [[' ' for _ in range(width)] for _ in range(height)]
        self.color_buffer = [[Colors.RESET for _ in range(width)] for _ in range(height)]
    
    def clear_buffer(self):
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.color_buffer = [[Colors.RESET for _ in range(self.width)] for _ in range(self.height)]
    
    def set_pixel(self, x, y, char, color):
        x, y = int(x), int(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char
            self.color_buffer[y][x] = color
    
    def render(self):
        # Clear screen
        print('\033[2J\033[H', end='')
        
        output = []
        for y in range(self.height):
            line = []
            current_color = Colors.RESET
            for x in range(self.width):
                if self.color_buffer[y][x] != current_color:
                    current_color = self.color_buffer[y][x]
                    line.append(current_color)
                line.append(self.buffer[y][x])
            line.append(Colors.RESET)
            output.append(''.join(line))
        
        print('\n'.join(output))

class FireworksShow:
    def __init__(self):
        self.terminal = Terminal(100, 30)
        self.fireworks = []
        self.rockets = []
        self.frame = 0
        self.firework_count = 0
        self.show_greeting = True
    
    def launch_rocket(self):
        x = random.randint(10, self.terminal.width - 10)
        target_y = random.randint(5, 15)
        color = Colors.random_color()
        self.rockets.append(Rocket(x, target_y, color))
        self.firework_count += 1
    
    def launch_firework(self, x, y, fw_type=None):
        if fw_type is None:
            fw_type = random.choice(['burst', 'ring', 'willow', 'heart'])
        self.fireworks.append(Firework(x, y, fw_type))
    
    def draw_greeting(self):
        messages = [
            "✨ शुभ दीपावली ✨",
            "Happy Diwali!",
            "May Your Life Be Filled With Light & Joy"
        ]
        
        colors = [Colors.GOLD, Colors.ORANGE, Colors.YELLOW]
        
        y_start = 10
        for i, msg in enumerate(messages):
            x_pos = (self.terminal.width - len(msg)) // 2
            y_pos = y_start + i * 2
            color = colors[i % len(colors)]
            
            if y_pos < self.terminal.height:
                for j, char in enumerate(msg):
                    self.terminal.set_pixel(x_pos + j, y_pos, char, color)
    
    def draw_diyas(self):
        diya_positions = [15, 30, 45, 60, 75, 85]
        diya = "🪔" if not IS_WINDOWS else "۝"
        
        for pos in diya_positions:
            if pos < self.terminal.width:
                flame_color = Colors.ORANGE if self.frame % 4 < 2 else Colors.YELLOW
                self.terminal.set_pixel(pos, self.terminal.height - 2, diya, flame_color)
                # Flame flicker
                if random.random() > 0.5:
                    self.terminal.set_pixel(pos, self.terminal.height - 3, '˄', Colors.YELLOW)
    
    def draw_stats(self):
        stats = f"Fireworks: {self.firework_count} | Active: {len(self.fireworks)} | Frame: {self.frame}"
        for i, char in enumerate(stats):
            if i < self.terminal.width:
                self.terminal.set_pixel(i, 0, char, Colors.CYAN)
    
    def update(self):
        self.frame += 1
        
        # Launch rockets periodically
        if self.frame % 30 == 0:
            self.launch_rocket()
        
        # Random extra rockets
        if random.random() > 0.95:
            self.launch_rocket()
        
        # Update rockets
        exploded_rockets = []
        for rocket in self.rockets:
            if rocket.update():
                exploded_rockets.append(rocket)
        
        # Create fireworks from exploded rockets
        for rocket in exploded_rockets:
            self.launch_firework(rocket.x, rocket.y)
            self.rockets.remove(rocket)
        
        # Update fireworks
        self.fireworks = [fw for fw in self.fireworks if fw.update()]
    
    def render(self):
        self.terminal.clear_buffer()
        
        # Draw diyas at bottom
        self.draw_diyas()
        
        # Draw greeting message (flashing effect)
        if self.show_greeting and (self.frame // 60) % 2 == 0:
            self.draw_greeting()
        
        # Draw rockets
        for rocket in self.rockets:
            # Draw trail
            for tx, ty in rocket.trail:
                self.terminal.set_pixel(tx, ty, '|', rocket.color)
            # Draw rocket
            self.terminal.set_pixel(rocket.x, rocket.y, '▲', rocket.color)
        
        # Draw fireworks
        for firework in self.fireworks:
            for particle in firework.particles:
                # Draw trail
                alpha = particle.life / particle.max_life
                if alpha > 0.7:
                    for tx, ty in particle.trail:
                        self.terminal.set_pixel(tx, ty, '·', particle.color)
                
                # Draw particle
                self.terminal.set_pixel(particle.x, particle.y, particle.char, particle.color)
        
        # Draw stats
        self.draw_stats()
        
        self.terminal.render()
    
    def run(self):
        print("\n" + "="*100)
        print(Colors.GOLD + Colors.BOLD + "🎆 DIWALI FIREWORKS CELEBRATION 🎆".center(100) + Colors.RESET)
        print("="*100)
        print(Colors.CYAN + "Press Ctrl+C to exit".center(100) + Colors.RESET)
        print("="*100 + "\n")
        time.sleep(2)
        
        # Initial burst
        for _ in range(3):
            self.launch_rocket()
        
        try:
            while True:
                self.update()
                self.render()
                time.sleep(0.05)  # ~20 FPS
        
        except KeyboardInterrupt:
            print("\n\n" + Colors.GOLD + "✨ Thank you for celebrating Diwali with us! ✨".center(100) + Colors.RESET)
            print(Colors.ORANGE + "शुभ दीपावली! Happy Diwali!".center(100) + Colors.RESET + "\n")

if __name__ == "__main__":
    show = FireworksShow()
    show.run()