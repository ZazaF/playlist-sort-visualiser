# playlist-sort-visualiser - Quick Sort Playlist Visualiser

## Chosen Problem
This project solves the **Playlist Vibe Builder** problem from the project guidelines. The app lets the user enter and edit a playlist of songs, then sort the playlist by either **energy** or **duration** using Quick Sort.

Each song includes:
- title
- artist
- energy score
- duration in seconds

The goal is to make the sorting process easy to understand by showing how Quick Sort changes the order of the playlist step by step.

## Chosen Algorithm
The algorithm used in this project is **Quick Sort**.

I chose Quick Sort because it is an efficient comparison-based sorting algorithm and it fits this playlist problem well. Since each song has sortable numeric values like energy and duration, Quick Sort can repeatedly compare songs, choose a pivot, partition the list, and recursively sort smaller sublists.

Quick Sort is also a strong choice for visual simulation because the user can clearly see:
- the pivot
- which songs are being compared
- which songs are swapped
- how the active subarray changes during sorting

## Demo
https://github.com/user-attachments/assets/c0999357-8b98-4a4f-8de5-2bb8751c83bc

https://github.com/user-attachments/assets/53f1a363-6bef-4f37-9b56-5240dceb1483

## Problem Breakdown & Computational Thinking

### Decomposition
The project is broken into smaller tasks:
1. collect playlist data from the user
2. validate each row of input
3. store songs in a structured format
4. let the user choose a sorting key
5. apply Quick Sort to the playlist
6. record each important sorting step
7. display the current step visually
8. show the final ranked playlist

### Pattern Recognition
Quick Sort repeats the same pattern:
- choose a pivot
- compare each element to the pivot
- move smaller elements to the left side
- move larger elements to the right side
- place the pivot in its correct position
- recursively repeat the process on smaller subarrays

This repeated compare-partition-recurse pattern is the main pattern used throughout the project.

### Abstraction
The app only shows the most important parts of the algorithm:
- active subarray
- pivot
- compared item
- swapped items
- current order of the songs
The app does not show low-level implementation details such as memory layout, because those are not necessary for understanding how Quick Sort works.

### Algorithm Design
**Input → Process → Output**

- **Input:** a table of songs and a selected sorting key
- **Process:** validate rows, run Quick Sort, record pivot/compare/swap steps
- **Output:** a visual step display, a current-step explanation, and the final ranked playlist

The app also includes controls to help the user interact with the simulation and understand the sorting process more clearly:
- Previous
- Next
- Autoplay
- Pause
- Reset
  
## Flowchart

<img width="655" height="910" alt="Flowchart" src="https://github.com/user-attachments/assets/b44d7055-4e7e-42a5-a050-8ab5ab4a276c" />

## Steps to Run
1. Download Python and make sure its the latest version https://www.python.org/downloads/
2. Open a Terminal and make sure that the required packages are installed (python, gradio): pip install -r requirments.txt
3. To run the app write; python app.py in the Terminal 
4. While the Terminal is still running, open the local Gradio link http://127.0.0.1:7860 in the browser
5. Run the app
   
## Requirements
gradio>=4.0.0

## Hugging face link 
https://huggingface.co/spaces/Farah-11/playlist-sort-visualiser

## Testing
Test 1: When given a playlist where multiple songs have the same energy or duration values, the app correctly handles the duplicates by keeping them grouped together and still sorting the rest of the playlist in ascending order. The visualiser continues to show the pivot, comparisons, and swaps without errors.
<img width="1362" height="831" alt="Screenshot 2026-04-15 at 11 18 22 PM" src="https://github.com/user-attachments/assets/8be6dda5-b11d-4a33-9b21-52cbb40e89bd" />

Test 2: When given a playlist with multiple songs, the app correctly sorts the songs by energy or duration based on the selected option. The final playlist is in ascending order, and the visualiser shows each step of Quick Sort, including pivot selection, comparisons, and swaps.
<img width="1294" height="832" alt="Screenshot 2026-04-15 at 10 44 26 PM" src="https://github.com/user-attachments/assets/46ea6cdf-1841-4df1-9e7f-7af69c621391" />

Test 3: When given invalid or incomplete input, such as blank song fields, non-numeric values, out-of-range energy values, or non-positive duration values, the app correctly rejects the input and displays a clear error message instead of failing.
<img width="1339" height="822" alt="Screenshot 2026-04-15 at 10 43 08 PM" src="https://github.com/user-attachments/assets/5a073c49-dc8e-4edf-a1f6-a804eab0734f" />

## Author & AI Acknowledgement 
Author: Farah Zaza

This project was created for CISC 121. 

Sources: Notes from CISC 121 course on OnQ and guidlines for this final project. 

AI Acknowledgment (Level 4): AI tools were used to assist with debugging, refining the Quick Sort implementation, and improving the Gradio interface. Specifically, AI helped with fixing issues related to input validation, implementing the step-by-step visualisation logic, and adding features like autoplay for the sorting simulation. All code was reviewed, tested, and fully understood by me, and I made modifications to ensure it met the project requirements, including improving the user interface, adding custom playlist data, and ensuring the algorithm followed Quick Sort logic without using built-in sorting functions. https://chatgpt.com/share/69e052d9-1300-83ea-9188-046f7aa60a03 
