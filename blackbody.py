import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad



h = 6.62607015e-34       
c = 2.99792458e8         
k = 1.380649e-23         
G = 6.67430e-11
sigma = 5.670374419e-8
M_sun = 1.989e30

def plancksformula(wavelength, T):
    exponent = (h * c) / (wavelength * k * T)
    numerator = 2 * h * c**2
    denominator = (wavelength**5) * (np.exp(exponent) - 1)
    return numerator / denominator


wavelength = np.linspace(1e-6, 3e-5, 1000)  

T = [500, 600, 700, 1500]

for i in T:
    intensity = plancksformula(wavelength, i)
    plt.plot(wavelength * 1e6, intensity, label=f"T = {i} K")

plt.xlabel("Wavelength in microns")
plt.ylabel("Spectral Radiance")
plt.title("Blackbody Radiation")
plt.legend()
plt.show()
