    
import sys
import matplotlib.pyplot as plt
from scipy import signal
from support.support_mp4 import generate_pdf

    
def run_analysis(self):
    self.cam_space = self.cam_space[:-1]
    self.cam_space = self.cam_space.interpolate(method='linear', limit_direction='forward')
    print(self.cam_space)
    Nmedf = 5
    camfdf = self.cam_space
    for _col in camfdf:
        camfdf[_col] = signal.medfilt(camfdf[_col], kernel_size=Nmedf)

    plt.title("ROM")
    plt.scatter(self.cam_space["X"], self.cam_space["Z"], c="r")
    plt.savefig(".//src//figure_scatter.png")
    plt.clf()

    plt.subplot(3, 1, 1)
    plt.title("Coordinates")
    plt.plot(self.cam_space["time"], self.cam_space["X"], label="X", c="r")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(self.cam_space["time"], self.cam_space["Y"], label="Y", c="y")

    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(self.cam_space["time"], self.cam_space["Z"], label="Z", c="b")

    plt.legend()

    plt.savefig(".//src//figure.png")
    a = generate_pdf(self)