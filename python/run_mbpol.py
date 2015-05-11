from __future__ import print_function
import configparser

from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import sys
import mbpol

try: # support for python 2
    from exceptions import KeyError
except:
    pass

if len(sys.argv) < 2:
    print("run_mbpol configurationfile.ini")
    sys.exit(1)

## Read configuration
config_filename = sys.argv[1]
config = configparser.ConfigParser()
print("Reading configuration from " + config_filename)
config.read(config_filename)

assert "system" in config.sections(), "ERROR: The configuration file needs a [system] section"

print("Loading positions from " + config["system"]["pdb_filename"])
pdb = app.PDBFile(config["system"]["pdb_filename"])

## Load the mbpol force field

forcefield = app.ForceField("mbpol.xml")

## Set nonbonded interaction

nonbonded = getattr(app, config["system"]["nonbonded"])
print("Configuring {} nonbonded interaction".format(config["system"]["nonbonded"]))
if config["system"]["nonbonded"] == "PME":
    boxDim = float(config["system"]["pme_box_size_nm"])
    boxSize = (boxDim, boxDim, boxDim) * unit.nanometer
    pdb.topology.setUnitCellDimensions(boxSize)

## Create the System, define an integrator, define the Simulation

system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.CutoffNonPeriodic, nonBondedCutoff=0.9*unit.angstrom)

temperature = float(config["system"]["temperature_k"])*unit.kelvin

try:
    system.addForce(mm.AndersenThermostat(temperature, float(config["thermostat"]["collision_rate_1overps"])/unit.picoseconds))
    print("Setting up thermostat")
except KeyError:
    print("Thermostat not defined")

try:
    system.addForce(mm.MonteCarloBarostat(
        float(config["barostat"]["pressure_atm"]) * unit.atmospheres,
        temperature,
        int(config["barostat"]["barostat_interval"])
    ))
    print("Setting up barostat")
except KeyError:
    print("Barostat not defined")

integrator = mm.VerletIntegrator(config.getfloat("integrator", "timestep_fs", fallback=1.)*unit.femtoseconds)

platform = mm.Platform.getPlatformByName('Reference')
simulation = app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)
simulation.context.computeVirtualSites()

## Local energy minimization
simulation_steps = config.getint("integrator", "production_steps", fallback=1)
equilibration_steps = config.getint("integrator", "equilibration_steps", fallback=1)

print("Setting up output files " + config["system"]["simulation_name"] + "[.pdb,.log]")
reporters = []
reporters.append(app.PDBReporter(config["system"]["simulation_name"] + ".pdb", config.getint("logging", "save_positions_every", fallback=1)))
reporters.append(app.StateDataReporter(config["system"]["simulation_name"] + ".log", config.getint("logging", "save_energy_every", fallback=1), step=True,
        potentialEnergy=True, temperature=True, progress=True, remainingTime=True,
        speed=True, totalSteps=simulation_steps+equilibration_steps, separator='\t'))

if config.getboolean("system", "local_minimization"):
    print("Running geometry optimization")
    from simtk.openmm import LocalEnergyMinimizer
    LocalEnergyMinimizer.minimize(simulation.context, 1e-1)

if config.has_section("integrator"):

    ## Run a constant energy simulation (Verlet integrator)

    print("Setting random velocities to {}".format(temperature))
    simulation.context.setVelocitiesToTemperature(temperature)
    # Equilibrate

    # Add a `reporter` that prints out the simulation status every 10%
    simulation.reporters.append(app.StateDataReporter(sys.stdout, max(1, int((simulation_steps+equilibration_steps)/10)), step=True,
        progress=True, remainingTime=True,
        speed=True, totalSteps=simulation_steps+equilibration_steps, separator='\t'))

    print("Running equilibration")
    simulation.step(equilibration_steps)
    print("Running simulation")

    for r in reporters:
        simulation.reporters.append(r)

    simulation.step(simulation_steps)

else:
    print("Computing forces and energy")
    state = simulation.context.getState(getForces=True, getEnergy=True, getPositions=True)

    for r in reporters:
        r.report(simulation, state)
