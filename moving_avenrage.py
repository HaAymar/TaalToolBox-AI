# Program to calculate moving average
arr = [1, 2, 3, 7, 9]
window_size = 3

i = 0
# Initialize an empty list to store moving averages
moving_averages = []

# Loop through the array to consider
# every window of size 3
while i < len(arr) - window_size + 1:

    # Store elements from i to i+window_size
    # in list to get the current window
    window = arr[i : i + window_size]

    # Calculate the average of current window
    window_average = round(sum(window) / window_size, 2)

    # Store the average of current
    # window in moving average list
    moving_averages.append(window_average)

    # Shift window to right by one position
    i += 1

print(moving_averages)
