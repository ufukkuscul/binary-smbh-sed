
r_in_single = 6 * r_g_total
r_out_single = 1000 * r_g_total

Mdot_single = 0.3 * eddington_mdot(M_total)
T0_single = T0_shakura(M_total, Mdot_single, r_in_single)


Llam_single = np.zeros_like(wavelengths)

for i, wl in enumerate(wavelengths):
    Llam_single[i] = disk_Llambda(wl, T0_single, r_in_single, r_out_single)

lamLlam_single = wavelengths * Llam_single

floor = 1e-8 * np.max(lamLlam_total)

single_plot = np.clip(lamLlam_single, floor, None)
binary_plot = np.clip(lamLlam_total,  floor, None)


plt.figure(figsize=(7, 5))

plt.plot(wavelengths * 1e6, binary_plot, label="Binary SMBH", linewidth=2)
plt.plot(wavelengths * 1e6, single_plot, '--', label="Single SMBH", linewidth=2)

plt.xscale("log")
plt.yscale("log")

plt.xlabel(r"log $\lambda$ ($\mu$m)")
plt.ylabel(r"log $\lambda L_\lambda$")

plt.legend()
plt.grid(True, alpha=0.3)

plt.show()
