import uproot

input_file = "DelphesOutput.root"
output_file = "output.pu14"
for array in uproot.iterate('DelphesOutput.root', ['Track/Track.PT', 'Track/Track.Eta', 'Track/Track.Phi']):
    event_count = len(array['Track/Track.PT'])

with uproot.open(input_file) as file:
    tree = file["Delphes"]

    weight = tree["Event.Weight"].array()
    track_size = tree["Track_size"].array()
    pid = tree["Track.PID"].array()
    pt = tree["Track.PT"].array()
    eta = tree["Track.Eta"].array()
    phi = tree["Track.Phi"].array()
    mass = tree["Track.Mass"].array()

    with open(output_file, "w") as out:
        for iE in range(event_count):
            out.write(f"# event {iE}\n")
            out.write(f"weight {weight[iE][0]}\n")
            
            for i in range(track_size[iE]):
                out.write(f"{pt[iE][i]} {eta[iE][i]} {phi[iE][i]} {mass[iE][i]} {pid[iE][i]} 0\n")
            
            out.write("end\n")
