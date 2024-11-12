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
for array in uproot.iterate(input_file, ['EFlowNeutralHadron/EFlowNeutralHadron.ET', 'EFlowNeutralHadron/EFlowNeutralHadron.Eta', 'EFlowNeutralHadron/EFlowNeutralHadron.Phi']):
    event_count = len(array['EFlowNeutralHadron/EFlowNeutralHadron.ET'])

with uproot.open(input_file) as file:
    tree = file["Delphes"]

    weight = tree["Event.Weight"].array()
    EFlowNeutralHadron_size = tree["EFlowNeutralHadron_size"].array()
    et = tree["EFlowNeutralHadron.ET"].array()
    eta = tree["EFlowNeutralHadron.Eta"].array()
    phi = tree["EFlowNeutralHadron.Phi"].array()
    e = tree["EFlowNeutralHadron.E"].array()

    with open(output_file, "w") as out:
        for iE in range(event_count):
            out.write(f"# event {iE}\n")
            out.write(f"weight {weight[iE][0]}\n")
            
            for i in range(EFlowNeutralHadron_size[iE]):
                out.write(f"{et[iE][i]} {eta[iE][i]} {phi[iE][i]} {e[iE][i]} 0 1\n")
            
            out.write("end\n")
