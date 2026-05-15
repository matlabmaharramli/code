from simulation import Simulation

sim = Simulation("parameters_solar.json", 10000, 100) # 1000 intervals, 1 Earth Year
sim.beeman_compute()
sim.determine_alignment(threshold=10)
sim.animate(interval=20, trail=True, show_alignment=True) # Very low FPS (interval=2000) to demonstrate alignment and allow possible screenshots

data = sim.return_alignment_data()


# Veryfying the values
for x, y in data.items():
    print(f"{x}: {y}")