import pygame
import numpy as np
import matplotlib.pyplot as plt


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 780))
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.data: np.ndarray = np.ndarray(0, dtype=np.int16)

    def updateData(self, data):
        self.data = np.concatenate((self.data, data))

    def run(self):
        cy = 0
        surf = pygame.Surface((100, 100))
        t = np.ndarray((1000, 600))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(
                self.font.render(str(self.data.size), True, (255, 255, 255)), (0, cy)
            )

            d = self.data

            if d.size > 80000:
                self.running = False
                break
            if d.size > 800:
                print(d.size - 800)
                d = d[:800]

            x = np.arange(0, d.size, dtype=np.int16)
            y = np.arange(0, d.size, dtype=np.int16)
            X, Y = np.meshgrid(x, y)

            if d.size != 0:
                v = np.int16(np.abs(d[y]) // 20)
                for i in range(v.size):
                    if v[i] < 0:
                        v[i] = 0
                    if v[i] > v.size:
                        v[i] = v.size

                # print(v)
                Z = np.zeros((d.size, d.size), dtype=np.int16)
                Z[X, v.size - v - 1] = 255
                surf = pygame.surfarray.make_surface(Z)

            self.screen.blit(surf, (25, 25))

            """t_audio = d.size / 4100
            times = np.linspace(0, t_audio, num=d.size)
            plt.figure(figsize=(15, 5))
            plt.plot(times, d)
            plt.title("Left Channel")
            plt.ylabel("Signal Value")
            plt.xlabel("Time (s)")
            plt.xlim(0, t_audio)
            plt.show()"""

            # print(self.data.size, self.data.shape)
            self.data = np.ndarray(0)

            cy += 0
            pygame.display.flip()
            self.clock.tick(60)
