import pandas as pd

ADR_CSV = pd.DataFrame({
    'R': [1, 2, 3, 4, 5],
    'SERIE': ['S1 R1', 'S1 R2', 'S1 R3', 'S1 R4', 'S1 R5'],
    'KG': [50, 50, 50, 50, 50],
    'D': [76.40, 92.52, 100.89, 79.57, 83.71],
    'VM': [0.56, 0.70, 0.77, 0.71, 0.78],
    'VMP': [0.56, 0.70, 0.96, 0.71, 0.81],
    'RM': [66.64, 80.20, 127.38, 81.37, 95.24],
    'P(W)': [274, 343, 377, 348, 382],
    'Perfil': ['Personal', 'Personal', 'Personal', 'Personal', 'Personal'],
    'Ejer.': ['Sentadilla profunda', 'Sentadilla profunda', 'Sentadilla profunda', 'Sentadilla profunda', 'Sentadilla profunda'],
    'Atleta': ['personal', 'personal', 'personal', 'personal', 'personal'],
    'Ecuacion': ['sesionsentadillaprofunda', 'sesionsentadillaprofunda', 'sesionsentadillaprofunda', 'sesionsentadillaprofunda', 'sesionsentadillaprofunda']
})


ADR_CSV_1 = pd.DataFrame({
    'R': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    'SERIE': ['S1 R1', 'S1 R2', 'S1 R3', 'S1 R4', 'S1 R5', 'S1 R6', 'S1 R7', 
              'S2 R1', 'S2 R2', 'S2 R3', 'S2 R4', 'S2 R5', 'S3 R1', 'S3 R2', 'S3 R3'],
    'KG': [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
    'D': [76.40, 92.52, 100.89, 79.57, 83.71, 81.99, 75.51, 36.75, 42.53, 
          52.36, 48.46, 74.68, 61.29, 56.07, 19.93],
    'VM': [0.56, 0.70, 0.77, 0.71, 0.78, 0.91, 0.69, 0.66, 0.83, 0.95, 0.89, 
           1.17, 1.34, 0.33, 0.20],
    'VMP': [0.56, 0.70, 0.96, 0.71, 0.81, 0.91, 0.77, 0.72, 0.93, 1.00, 1.01, 
            1.21, 1.41, 0.33, 0.20],
    'RM': [66.64, 80.20, 127.38, 81.37, 95.24, 114.56, 89.18, 82.58, 119.37, 
           139.84, 143.34, 283.74, 6959.90, 51.95, 46.11],
    'P(W)': [274, 343, 377, 348, 382, 446, 338, 323, 407, 466, 436, 573, 657, 
             162, 98],
    'Perfil': ['Personal']*15,
    'Ejer.': ['Sentadilla profunda']*15,
    'Atleta': ['personal']*15,
    'Ecuacion': ['sesionsentadillaprofunda']*15
})