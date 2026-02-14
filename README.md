# NASA-Battery-Data-Analysis
A data pipeline for extracting, cleaning, and validating SOH from NASA battery datasets using Coulomb Counting method.
# 🔋 NASA Li-ion Battery SOH Estimation

## Project Overview
This project implements a **Coulomb Counting (Ah Integration)** algorithm to estimate the State of Health (SOH) of Li-ion batteries using the **NASA PCoE Dataset (B0005)**.

The goal is to validate the accuracy of edge-computing algorithms for future **Web3 Battery Passport** applications.

## 📊 Key Results
We compared the calculated capacity with NASA's ground truth values. The curves align perfectly, proving the robustness of the algorithm.

![Validation Plot](comparison_plot.png) 
*(Ensure you upload your image and check the filename)*

## 🛠️ Tech Stack
- **Python**: Core logic
- **Pandas**: Data cleaning & ETL
- **NumPy/SciPy**: Trapezoidal integration
- **Matplotlib**: Visualization

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the script: `python processing_data.py`
