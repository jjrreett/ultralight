
# %%
import math
# %%
# Constants
sec = 1
kg = 1
n = 1
m = 1
m2 = m*m
m3 = m*m*m
lbm = 0.453592 * kg
lbf = 4.44822 * n
knots = 0.514444 * m / sec
ft = 0.3048 # m
ft2 = ft*ft
ft3 = ft*ft*ft
gal = 0.133681 * ft3
g = 9.81 * m / sec**2
fuel_density = 780 * kg / m3 # https://www.engineeringtoolbox.com/fuels-densities-specific-volumes-d_166.html
rho = 1.225 * kg / m3 # air density at sea level

# %% [markdown]

# # Design Requirements

# ## Regulatory

# ### Weight
# In a powered configuration, the vehicle shall weigh less than 254 pounds empty weight.
# In a non-powered configuration, the vehicle shall weigh less than 155 pounds empty weight.
# Note: excludes floats and safety devices which are intended for deployment in a potentially catastrophic situation. 

# ### Fuel Capacity
# The vehicle shall have a fuel capacity not exceeding 5.0 U.S. gallons.

# ### Max Airspeed
# The vehicle shall have not be capable of more than 55 knots calibrated airspeed at full power in level flight.

# ### Stall Speed
# The vehicle shall have a stall speed of no more than 24 knots calibrated airspeed in the landing configuration.

# ## Structural

# ### Factor of safety
# The vehicle shall be designed to withstand an ultimate load 1.5 times the maximum expected load.
# _Reference:_ Shanley, F. R. (1962, February). Historical note on the 1.5 Factor of Safety for Aircraft Structures. Journal of the Aerospace Sciences, 29(2), 243-244.

# ### Maximum Load
# The vehicle shall be designed to withstand a maximum load of 4 g's.

# ## Mission
# ### Pilot Weight
# The vehicle shall be designed to carry a pilot weighing between 150 and 150 pounds.

# %% [markdown]
# ## Design Goals

# ### Powered and glider configurations
# I want the plane to be able to operate as a glider and a powered vehicle. This means the propulsion systems should be easily removable. Assuming the worst case of 254 lbm, we shall compute the max power required for the vehicle. From there we can perform a trade study to determine propulsion system mass. Given this mass we can recompute the max weight of the vehicle for structural analysis.

# %%
# Requirements
weight_empty_max_powered = 254 * lbf
weight_empty_max_glider = 155 * lbf
airspeed_max = 55 * knots
stall_speed_max = 24 * knots
fos = 1.5
max_load_g = 4
pilot_weight_min = 150 * lbf
pilot_weight_max = 250 * lbf
fuel_mass = 5 * gal * fuel_density

# %% [markdown]
# # Initial estimates

# ## Gross Takeoff Weight
gross_takeoff_weight_max = weight_empty_max_powered + pilot_weight_max + fuel_mass * g
gross_takeoff_weight_max / lbf

# %%
# Redefine stall speed max for better performance slop soaring performance. Based on Goat 1 design drawings

goat_weight = (140 * lbf + 170 * lbf)
goat_wing_area = 174 * ft2
goat_wing_loading = goat_weight / goat_wing_area
goat_Cl = 1.6 # https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_103-7.pdf Appendix 2
goat_q = goat_wing_loading / goat_Cl
goat_v_stall = math.sqrt(goat_q / 0.5 / rho)
stall_speed_max = goat_v_stall * 1.12
stall_speed_max / knots
# %% 
# Power loading
# Weight / horsepower

power_loading_lbfphp = 325 * (airspeed_max / knots) ** -0.75 # TODO add reference
power_loading_lbfphp
# %%
power = gross_takeoff_weight_max / lbf / power_loading_lbfphp
power

propulsion_system_mass = 33 * lbf # https://aerolight.com/product/vittorazi-moster-185-silent-silent-d-s-plus-plus-d-s-and-factory/
# This only produces 25 hp, but it is a good starting point for the iterations
gross_takeoff_weight_max = (weight_empty_max_glider + pilot_weight_max + fuel_mass + propulsion_system_mass)

power = gross_takeoff_weight_max / lbf / power_loading_lbfphp
power

propulsion_system_mass = 2 * 10 * kg # https://www.miniplane-usa.com/pages/motor.htm
gross_takeoff_weight_max = (weight_empty_max_glider + pilot_weight_max + fuel_mass + propulsion_system_mass)

power = gross_takeoff_weight_max / lbf / power_loading_lbfphp
power

# The solution has converged
print(f"{gross_takeoff_weight_max/lbf = } lbf, {power = } hp")

# %%
# wing loading
# Weight / wing area

q = 0.5 * rho * stall_speed_max ** 2 # dynamic pressure
# https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_103-7.pdf Appendix 2
# Lift factor for a double surface camber = 1.4
Cl = 1.4
wing_loading = q * Cl
wing_loading / (lbf/ft2)



# %%
wing_area = gross_takeoff_weight_max / wing_loading
wing_area / ft2
# %%
