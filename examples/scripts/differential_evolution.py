import pbparam
import pybamm
import pandas as pd

model = pybamm.lithium_ion.SPMe()
parameter_values = pybamm.ParameterValues("Chen2020")

sim0 = pybamm.Simulation(model, parameter_values=parameter_values)
sol = sim0.solve([0, 3600])

data = pd.DataFrame(
    {
        "Time [s]": sol["Time [s]"].entries,
        "Terminal voltage [V]": sol["Terminal voltage [V]"].entries,
    }
)

sim = pybamm.Simulation(model, parameter_values=parameter_values)

opt = pbparam.OptimisationProblem(
    sim,
    data,
    {
        "Negative electrode diffusivity [m2.s-1]": (5e-15, (2.06e-16, 2.06e-12)),
        # "Total heat transfer coefficient [W.m-2.K-1]": (20, (0.1, 1000)),
        # (
        #     "Positive current collector specific heat capacity [J.kg-1.K-1]",
        #     "Negative current collector specific heat capacity [J.kg-1.K-1]",
        #     "Negative electrode specific heat capacity [J.kg-1.K-1]",
        #     "Separator specific heat capacity [J.kg-1.K-1]",
        #     "Positive electrode specific heat capacity [J.kg-1.K-1]",
        # ): (2.85e3, (2.85, 2.85e6)),
    },
)

solver = pbparam.ScipyDifferentialEvolution(
    extra_options={"workers": -1, "polish": True, "updating": "deferred"}
)

result = solver.optimise(opt)

print(result.x, result.fun, result.solve_time)

result.plot()
