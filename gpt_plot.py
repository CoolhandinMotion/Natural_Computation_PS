
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
import pandas as pd

def plot_ea_convergence(
        all_logs: Dict[str, List[pd.DataFrame]],
        num_interp_points: int = 500,
        title: str = None,
        xlabel: str = 'Number of Fitness Evaluations',
        ylabel: str = 'Best Found Fitness',
        figsize: tuple = (15, 9),
        show_std: bool = True,
        style: str = 'seaborn-v0_8-whitegrid',
        palette: str = 'husl'
):
    """
    Plots the convergence of different EA configurations using interpolated fitness curves.

    Parameters:
        all_logs (dict): A dictionary mapping configuration names to lists of pandas DataFrames.
                         Each DataFrame must contain columns:
                         - 'Gesamte_Fitness_Evaluations'
                         - 'Beste_Fitness_Generation'
        num_interp_points (int): Number of points to interpolate across for plotting.
        title (str): Plot title. Defaults to a standard title if None.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        figsize (tuple): Size of the figure.
        show_std (bool): Whether to show shaded standard deviation region.
        style (str): Matplotlib style to use.
        palette (str): Seaborn color palette.
    """
    plt.style.use(style)
    sns.set_palette(palette)

    plt.figure(figsize=figsize)
    if title is None:
        title = f'Convergence Plot (averaged over runs)'
    plt.title(title, fontsize=16, weight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    # Determine max evaluations across all logs
    max_evals = max(
        (log['Gesamte_Fitness_Evaluations'].max()
         for logs in all_logs.values()
         for log in logs if not log.empty),
        default=0
    )

    if max_evals == 0:
        print("No valid logs found with evaluation data.")
        return

    eval_points = np.linspace(0, max_evals, num_interp_points)

    for config_name, logs in all_logs.items():
        interpolated_fitnesses = []

        for log in logs:
            if log.empty:
                continue
            # Ensure unique evaluation points (np.interp requires increasing x)
            log_clean = log.drop_duplicates(subset='Gesamte_Fitness_Evaluations', keep='first')
            try:
                interp = np.interp(
                    eval_points,
                    log_clean['Gesamte_Fitness_Evaluations'],
                    log_clean['Beste_Fitness_Generation']
                )
                interpolated_fitnesses.append(interp)
            except Exception as e:
                print(f"Interpolation failed for {config_name}: {e}")

        if not interpolated_fitnesses:
            print(f"No valid data for configuration: {config_name}")
            continue

        interpolated_fitnesses = np.array(interpolated_fitnesses)
        mean_fitness = np.mean(interpolated_fitnesses, axis=0)
        std_fitness = np.std(interpolated_fitnesses, axis=0)

        plt.plot(eval_points, mean_fitness, label=config_name)
        if show_std:
            plt.fill_between(
                eval_points,
                mean_fitness - std_fitness,
                mean_fitness + std_fitness,
                alpha=0.15
            )

    plt.legend()
    plt.tight_layout()
    plt.show()
