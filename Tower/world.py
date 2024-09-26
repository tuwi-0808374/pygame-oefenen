import pygame

class World():
    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image

    def process_data(self):
        # look through data to extract relevant data
        for layer in self.level_data['layers']:
            if layer['name'] == 'waypoints':
                for obj in layer['objects']:
                    waypoint_data = obj['polyline']
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        # iterate to waypoint to extract individual sets of x and y coordinates
        for point in data:
            temp_x = point['x']
            temp_y = point['y']
            self.waypoints.append((temp_x, temp_y))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
