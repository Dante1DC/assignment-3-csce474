# Setup
Run the following to ensure you have the right packages:
`pip install pandas matplotlib scipy arff`

# Usage
Run `python kmeans.py` to get started.

When the program runs, you'll be prompted to enter 4 variables:
- Filename (the file used for analysis)
- K (the max amount of clusters that will be analyzed)
- Epsilon (the cutoff threshold for cluster errors between runs)
- Iterations (the max amount of analytical iterations for each cluster)

For the graph that visualizes runtime over dataset size, we use a "stride" variable so that the algorithm doesn't have to compute over every size 1...n. It is 100 by default, but you can change it in the code (Line 161)

The dataset we ran our analysis on, and wrote our report over, is called "fruitfly.arff"
