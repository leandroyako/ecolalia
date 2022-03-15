# import required module
import os

# Create an empty dictionary
d = dict()

# assign directory
directory = '../timestamps'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):   
        # this will return a tuple of root and extension
        split_tup = os.path.splitext(f)
        # select txt files
        if split_tup[1] == '.txt':
            text = open(f, "r")   
            # Loop through each line of the file
            for line in text:
                # Remove the leading spaces and newline character
                line = line.strip()
            
                # Convert the characters in line to 
                # lowercase to avoid case mismatch
                line = line.lower()
            
                # Split the line into words
                words = line.split(" ")
            
                # Iterate over each word in line
                for word in words:
                    # Check if the word is already in dictionary
                    if word in d:
                        # Increment count of word by 1
                        d[word] = d[word] + 1
                    else:
                        # Add the word to dictionary with count 1
                        d[word] = 1

word_list = sorted(d.items(), key=lambda x:x[1])
word_sorted = dict(word_list)

# Print the contents of dictionary
for key in word_sorted:
    item = key + ":" + str(word_sorted[key])
    #print(item)
    f = open("ocurrences.txt", "a")
    f.write(item)
    f.write("\n")
    
f.close()