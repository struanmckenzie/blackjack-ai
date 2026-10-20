import os
import re
import csv

if __name__ == "__main__":
    directory_dfs = 'solvedDFS'
    directory_bfs = 'solvedBFS'
    directory_a_star = 'solvedAStar'
    directory_greedy = 'solvedGreedy'

    directories = [directory_dfs, directory_bfs, directory_a_star, directory_greedy]
    dimensions = {}
    first = True
    results = []

    for directory in directories:
        _, algorithm = directory.split("solved")
        image_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.png')]
        for path in image_paths:
            filename = os.path.basename(path)
            pattern = r"maze(?P<maze>\d+)_dim(?P<dimension>\d+) e=(?P<explored>\d+) p=(?P<path>\d+) t=(?P<time>\d+.\d+)"

            match = re.search(pattern, filename)
            if match:
                results.append({
                    "maze": match.group("maze"),
                    "dimension": match.group("dimension"),
                    "pixel_size": int(match.group("dimension")) * 2 + 1,
                    "algorithm": algorithm,
                    "explored": match.group("explored"),
                    "path": match.group("path"),
                    "execution_time": match.group("time")

                })
            else:
                print("Error")

    results.sort(key=lambda row: row["maze"])
    with open("maze_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())

        writer.writeheader()
        writer.writerows(results)
