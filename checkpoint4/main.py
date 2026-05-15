from traffic import Traffic

N = int(input("Enter the length of the road:"))
niter = int(input("Enter the number of iterations:"))
density = float(input("Enter the car density:"))


traffic = Traffic(N, niter, density)


traffic.display()
traffic.simulate()
traffic.plot_avg_v()
print(traffic.avg_v)