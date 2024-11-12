import uproot
import argparse

parser = argparse.ArgumentParser(description='Delphes Root Reader')
parser.add_argument('-i','--input', help='Input file name', required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)

args = parser.parse_args()

# print values
#print('*********Initialization**********')
#print('Input file:\t%s' % args.input)
#print('Output file: \t%s' % args.output)

input_file = args.input
output_file = args.output
for array in uproot.iterate(input_file, ['Particle/Particle.Px', 'Particle/Particle.Py', 'Particle/Particle.Pz']):
    event_count = len(array['Particle/Particle.Px'])
print(event_count)
with uproot.open(input_file) as file:
    tree = file["Delphes"]

    #weight = tree["Event.Weight"].array()
    particle_size = tree["Particle_size"].array()
    pid = tree["Particle.PID"].array()
    px = tree["Particle.Px"].array()
    py = tree["Particle.Py"].array()
    pz = tree["Particle.Pz"].array()
    pt = tree["Particle.PT"].array()
    eta = tree["Particle.Eta"].array()
    phi = tree["Particle.Phi"].array()
    mass = tree["Particle.Mass"].array()
    status = tree["Particle.Status"].array()

    with open(output_file, "w") as out:
        for iE in range(event_count):
            out.write(f"# event {iE}\n")
            #out.write(f"weight {weight[iE][0]:.7f}\n")
            
            for i in range(particle_size[iE]):
                if (eta[iE][i]>-3.0 and eta[iE][i]<3.0 and pt[iE][i]>0.3 and status[iE][i]==1):
                    out.write(f"{px[iE][i]:.6f} {py[iE][i]:.6f} {pz[iE][i]:.6f} {mass[iE][i]/1000.:.6f} {pid[iE][i]} 0\n")
            
            out.write("end\n")
