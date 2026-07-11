import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad



h = 6.62607015e-34       
c = 2.99792458e8         
k = 1.380649e-23         
G = 6.67430e-11
sigma = 5.670374419e-8
M_sun = 1.989e30

def planck_lambda(wavelength, T):
    exponent = (h * c) / (wavelength * k * T)
    numerator = 2 * h * c**2
    denominator = (wavelength**5) * (np.exp(exponent) - 1)
    return numerator / denominator

def integrate(r, wavelength, T):
    return planck_lambda(wavelength, T) * 2 * np.pi * r

def disk_sed_fixed_T(wavelength, T, inner, outer):
    result = quad(integrate, inner, outer, args=(wavelength, T))
    return result

wavelengths = np.linspace(1e-9, 3e-6, 500)
M = 10**9
risco = (30 * G * M ) / c**2
T = 10000
innerradius = risco
outerradius = 100

sed_values = []

for wl in wavelengths:
    sed = disk_sed_fixed_T(wl, T, innerradius, outerradius)
    sed_values.append(sed)

sed_values = np.array(sed_values)

plt.plot(wavelengths, sed_values)
plt.xscale('log')
plt.yscale('log')

plt.title("Single Accretion Disk SED (Fixed Temperature)")
plt.show()



def planck_lambda(wavelength, T):
    exponent = (h * c) / (wavelength * k * T)
    numerator = 2 * h * c**2
    denominator = (wavelength**5) * (np.exp(exponent) - 1)
    return numerator / denominator

def temperaturechange(r, T0, r_in):
    return T0 * (r / r_in)**(-3/4)

def disk_integrand(r, wavelength, T0, r_in):
    T_r = temperaturechange(r, T0, r_in)
    return planck_lambda(wavelength, T_r) * 2 * np.pi * r

def disk_sed_variable_T(wavelength, T0, r_in, r_out):
    result = quad(disk_integrand, r_in, r_out, args=(wavelength, T0, r_in))
    return result

wavelengths = np.linspace(1e-9, 3e-6, 500)

T0 = 50000
innerradius = 1
outerradius1 = 100
outerradius2 = 500000

sed_values_1 = []
sed_values_2 = []

for wl in wavelengths:
    sed1 = disk_sed_variable_T(wl, T0, innerradius, outerradius1)
    sed2 = disk_sed_variable_T(wl, T0, innerradius, outerradius2)
    sed_values_1.append(sed1)
    sed_values_2.append(sed2)

sed_values_1 = np.array(sed_values_1)
sed_values_2 = np.array(sed_values_2)

plt.figure()   

plt.plot(wavelengths * 1e6, sed_values_1, label="r_out = 100")
plt.plot(wavelengths * 1e6, sed_values_2, label="r_out = 500000")

plt.xlabel("Wavelength (microns)")
plt.ylabel("Disk Emission")
plt.title("Single Quasar Accretion Disk SED")
plt.legend()

plt.show()
