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

def temperaturechange(r, T0):
    return T0 * r**(-3/4)

def disk_integrand(r, wavelength, T0):
    T_r = temperaturechange(r, T0)
    return planck_lambda(wavelength, T_r) * 2 * np.pi * r

def disk_sed_variable_T(wavelength, T0, r_in, r_out):
    result = quad(disk_integrand, r_in, r_out, args=(wavelength, T0))
    return result

wavelengths = np.linspace(1e-9, 3e-6, 500)

T0 = 50000
outerradius = 500000

inner_single = 1
inner_binary = 100

sed_single = []
sed_binary = []

for wl in wavelengths:
    sed_single.append(disk_sed_variable_T(wl, T0, inner_single, outerradius))
    sed_binary.append(disk_sed_variable_T(wl, T0, inner_binary, outerradius))

sed_single = np.array(sed_single)
sed_binary = np.array(sed_binary)

plt.figure()
plt.plot(wavelengths * 1e6, sed_single, label="Single quasar disk")
plt.plot(wavelengths * 1e6, sed_binary, label="Circumbinary disk")
plt.xlabel("Wavelength")
plt.ylabel("Disk emission")
plt.title("SED comparison: single vs circumbinary Disk")
plt.legend()
plt.show()

"""----------------------------------------Part 4 ----------------------------------------"""

# Black hole parameters
M_total = 1e8 * M_sun
M1 = M_total / 2
M2 = M_total / 2

r_g1 = G * M1 / c**2
r_g2 = G * M2 / c**2
r_g_total = G * M_total / c**2
a_binary = 100 * r_g_total

# Disk radii
r_circum_in  = 2.0 * a_binary
r_circum_out = 500 * r_g_total
r_mini_in1   = 6  * r_g1
r_mini_out1  = 50 * r_g1
r_mini_in2   = 6  * r_g2
r_mini_out2  = 50 * r_g2

# Temperature normalization
def eddington_mdot(M):
    L_edd = 1.26e31 * (M / M_sun)
    return L_edd / (0.1 * c**2)

def T0_shakura(M, Mdot, r_in):
    return (3 * G * M * Mdot / (8 * np.pi * sigma * r_in**3)) ** 0.25

Mdot1       = 0.1 * eddington_mdot(M1)
Mdot2       = 0.1 * eddington_mdot(M2)
Mdot_circum = 0.3 * eddington_mdot(M_total)

T0_circum = T0_shakura(M_total, Mdot_circum, r_circum_in)
T0_mini1  = T0_shakura(M1, Mdot1, r_mini_in1)
T0_mini2  = T0_shakura(M2, Mdot2, r_mini_in2)

print(f"T0 circumbinary : {T0_circum:.2e} K")
print(f"T0 mini disk 1  : {T0_mini1:.2e} K")
print(f"T0 mini disk 2  : {T0_mini2:.2e} K")

# Physics
def planck_lambda(wavelength, T):
    exponent = (h * c) / (wavelength * k * T)
    return (2 * h * c**2) / (wavelength**5 * (np.exp(np.clip(exponent, 0, 700)) - 1))

def temperaturechange(r, T0, r_in):
    return T0 * (r / r_in)**(-3/4) * (1 - np.sqrt(r_in / r))**0.25

def disk_integrand(r, wavelength, T0, r_in):
    T_r = temperaturechange(r, T0, r_in)
    if T_r < 10:
        return 0.0
    return planck_lambda(wavelength, T_r) * 2 * np.pi * r

def disk_sed(wavelength, T0, r_in, r_out):
    result, _ = quad(disk_integrand, r_in, r_out,
                     args=(wavelength, T0, r_in), limit=100)
    return result

# ── KEY FIX: log-spaced wavelengths from 1nm to 3 microns ────────────────────
wavelengths = np.logspace(np.log10(1e-9), np.log10(3e-6), 500)

sed_circum = np.zeros(len(wavelengths))
sed_mini1  = np.zeros(len(wavelengths))
sed_mini2  = np.zeros(len(wavelengths))

for i, wl in enumerate(wavelengths):
    sed_circum[i] = disk_sed(wl, T0_circum, r_circum_in, r_circum_out)
    sed_mini1[i]  = disk_sed(wl, T0_mini1,  r_mini_in1,  r_mini_out1)
    sed_mini2[i]  = disk_sed(wl, T0_mini2,  r_mini_in2,  r_mini_out2)

sed_total = sed_circum + sed_mini1 + sed_mini2

# ── KEY FIX: normalize each component so humps are visible ───────────────────
def safe_norm(arr):
    m = np.max(arr)
    return arr / m if m > 0 else arr

sed_circum_n = safe_norm(sed_circum)
sed_mini1_n  = safe_norm(sed_mini1)
sed_mini2_n  = safe_norm(sed_mini2)
sed_total_n  = safe_norm(sed_total)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: normalized to see the shape (matches your sketch)
ax = axes[0]
ax.plot(wavelengths * 1e6, sed_total_n,   label="Total",             linewidth=2)
ax.plot(wavelengths * 1e6, sed_circum_n, '--', label=f"Circumbinary (T0={T0_circum:.1e} K)")
ax.plot(wavelengths * 1e6, sed_mini1_n,  ':',  label=f"Mini disk 1  (T0={T0_mini1:.1e} K)", linewidth=2)
ax.plot(wavelengths * 1e6, sed_mini2_n,  '-.',  label=f"Mini disk 2  (T0={T0_mini2:.1e} K)", linewidth=2)
ax.set_xscale("log")
ax.set_xlabel("Wavelength (μm)")
ax.set_ylabel("Normalized Emission")
ax.set_title("Normalized SED")
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Right: raw log-log (physical)
ax2 = axes[1]
ax2.plot(wavelengths * 1e6, sed_total,   label="Total",             linewidth=2)
ax2.plot(wavelengths * 1e6, sed_circum, '--', label="Circumbinary")
ax2.plot(wavelengths * 1e6, sed_mini1,  ':',  label="Mini disk 1", linewidth=2)
ax2.plot(wavelengths * 1e6, sed_mini2,  '-.',  label="Mini disk 2", linewidth=2)
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("Wavelength (μm)")
ax2.set_ylabel("Disk Emission")
ax2.set_title("Physical SED (log-log)")
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

plt.suptitle("Binary SMBH SED — M_total=1e8 M☉, equal mass, a=100 r_g", fontsize=11)
plt.tight_layout()
plt.show()
