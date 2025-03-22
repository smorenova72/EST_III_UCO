import math
import csv

k = 4
label_count = 4

with open('data.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

train = [row for row in data if row[-1] == "Yes"]
test = [row for row in data if row[-1] == "No"]

label_row = data[0].index('label')

centroids = {}

def get_centroids():

    for i in range(0, label_count):
        centroids[i] = [0] * len(data[0])

    for current_label in range(0, label_count):
        filtered = [row for row in train if str(row[label_row]) == str(current_label)]

        for i in range(0,len(filtered)):
            for j in range(0, len(filtered[i])):
                try:
                    centroids[current_label][j] += float(filtered[i][j])/len(filtered)
                except:
                    centroids[current_label][j] = 0

def get_distance(centroid, row):
    distance = 0

    for i in range(0, len(centroid)):
        if (i != label_row):
            try:
                distance += abs(float(row[i]) - float(centroid[i])) ** 2
            except:
                distance += 0

    return math.sqrt(distance)

def reassign_labels():
    swap = False

    for row in train:
        distances = []

        for l in range (0, label_count):
            distances.append(get_distance(centroids[l], row))

        min_dist = distances.index(min(distances))
        if row[label_row] != min_dist:
            row[label_row] = min_dist
            swap = True

    return swap

def perform_k_means():
    it = 0
    get_centroids()
    for i in range(0, k):
        it = i+1
        swap = reassign_labels()
        get_centroids()
        if not swap: break
    print("Iteration",it)

perform_k_means()

with open('k_means.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    for row in train:
        writer.writerow(row)

print("Training written to k_means.csv")

# TESTING

def assign_closest_city():
    output = [["ID","label"]]

    for test_row in test:
        centroid_distances = {}

        for label in range(0, label_count):
            centroid_distances[label] = get_distance(centroids[label], test_row)

        closest_centroid = min(centroid_distances, key=centroid_distances.get)
        test_row[label_row] = closest_centroid

        city_distances = {}

        for train_row in train:
            if train_row[label_row] == test_row[label_row]:
                city_distances[train_row[0]] = get_distance(train_row, test_row)

        closest_city = min(city_distances, key=city_distances.get)
        output.append([test_row[0],closest_city])

    with open('k_means_pred.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for row in output:
            writer.writerow(row)

    print("Prediction written to k_means_pred.csv")


assign_closest_city()
print(test)
