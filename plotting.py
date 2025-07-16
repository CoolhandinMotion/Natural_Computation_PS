
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from numpy.typing import NDArray
from utils import DataType
import numpy as np
import seaborn as sns
import pandas as pd
from typing import Dict,List

DATA_2_PLOT_LIM =  {DataType.KROA100: {'xlim': (-500,4500), 'ylim':(-500,2500)},
                    DataType.BERLIN52: {'xlim': (-500,2000), 'ylim':(-200,1400)}}

DATA_2_PLOT_STRIDE =  {DataType.KROA100: {'xstride': 500, 'ystride':500},
                    DataType.BERLIN52: {'xstride': 500, 'ystride':200}}

def plot_ea_convergence(
        all_logs: Dict[str, List[pd.DataFrame]],
        n_runs:int,
        save_name:str |None,
        num_interp_points: int = 500,
        title: str = None,
        xlabel: str = 'Number of Fitness Evaluations',
        ylabel: str = 'Best Found Fitness',
        fig_size: tuple[float,float] = (15, 9),
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
        fig_size (tuple): Size of the figure.
        show_std (bool): Whether to show shaded standard deviation region.
        style (str): Matplotlib style to use.
        palette (str): Seaborn color palette.
    """
    plt.style.use(style)
    sns.set_palette(palette)

    plt.figure(figsize=fig_size)
    if title is None:
        title = f'Convergence Plot (averaged over {n_runs} runs)'
    plt.title(title, fontsize=16, weight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)

    # Determine max evaluations across all logs
    max_evals = max(
        (log['Total_Fitness_Evaluations'].max()
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
            log_clean = log.drop_duplicates(subset='Total_Fitness_Evaluations', keep='first')
            try:
                interp = np.interp(
                    eval_points,
                    log_clean['Total_Fitness_Evaluations'],
                    log_clean['Best_Fitness_Generation']
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
    if save_name:
        plt.savefig(f"./output/{save_name}_convergence.png")
        plt.close()
        return
    plt.show()

def plot_city_tour(all_results: dict,
                   best_tours: dict,
                   coords: NDArray,
                   data_type: DataType,
                   save_name: str |None,
                   fig_size: tuple[float, float] = (10, 10)):
    best_overall_fitness = float('inf')
    best_overall_tour = None
    best_overall_key = ""
    plt.figure(figsize=fig_size)

    for key, fitness_list in all_results.items():
        if not fitness_list:
            continue
        min_fitness_in_key = min(fitness_list)
        if min_fitness_in_key < best_overall_fitness:
            best_overall_fitness = min_fitness_in_key
            best_overall_tour = best_tours[key]
            best_overall_key = key

    print(f"\nBest tour found comes from '{best_overall_key}' with a length of {best_overall_fitness:.2f}")

    plt.title(f'Best tour found for {data_type.value} ({best_overall_key})', fontsize=16, weight='bold')

    # Plot cities
    plt.scatter(coords[:, 0], coords[:, 1], c='red', zorder=2, label='Cities')

    # Plot tour
    if best_overall_tour:
        # Close the tour for visualization
        plot_tour = best_overall_tour + [best_overall_tour[0]]
        tour_coords = coords[plot_tour]
        plt.plot(tour_coords[:, 0], tour_coords[:, 1], 'b-', zorder=1, label='Best route')
    else:
        print("No valid tour found for visualization.")

    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend()
    plt.grid(True)
    y_lim = DATA_2_PLOT_LIM[data_type]['ylim']
    x_lim = DATA_2_PLOT_LIM[data_type]['xlim']
    plt.ylim(y_lim)
    plt.xlim(x_lim)
    x_stride = DATA_2_PLOT_STRIDE[data_type]['xstride']
    y_stride = DATA_2_PLOT_STRIDE[data_type]['ystride']
    plt.gca().xaxis.set_major_locator(MultipleLocator(x_stride))
    plt.gca().yaxis.set_major_locator(MultipleLocator(y_stride))
    if save_name:
        plt.savefig(f"./output/{save_name}_tour.png")
        plt.close()
        return
    plt.show()
