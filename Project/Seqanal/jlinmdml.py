__author__ = 'Kavin'



# Parse the file which was already split into split_list
with open("seq.txt", "r") as lines:
    with open("seq2.txt", "w") as output:
        for list in lines:
            split_list = list.split()
            header = "".join(split_list[0:2])
            seq = split_list[2]
            disorder = split_list[4]
            # Create the new disorder string
            new_disorder = ["Disorder:\nPosi\tR"]
            for i, x in enumerate(disorder):
                if x == "X":
                    # Appends of the form: "AminoAcid Position"
                    new_disorder.append("{}\t{}".format(i, seq[i]))

            new_disorder = "\n".join(new_disorder)

            # Output the modified file
            output.write("\n".join([header, seq, new_disorder]) + "\n\n")