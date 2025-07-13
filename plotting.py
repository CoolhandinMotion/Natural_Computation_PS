
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from numpy.typing import NDArray
from utils import DataType

DATA_2_PLOT_LIM =  {DataType.KROA100: {'xlim': (-500,4500), 'ylim':(-500,2500)},
                    DataType.BERLIN52: {'xlim': (-500,2000), 'ylim':(-200,1400)}}

DATA_2_PLOT_STRIDE =  {DataType.KROA100: {'xstride': 500, 'ystride':500},
                    DataType.BERLIN52: {'xstride': 500, 'ystride':200}}

def plot_city_tour(all_results:dict,
                   best_tours:dict,
                   coords:NDArray,
                   data_type:DataType,
                   fig_size:tuple[float,float] = (10, 10)):

    best_overall_fitness = float('inf')
    best_overall_tour = None
    best_overall_key = ""
    plt.figure(figsize=fig_size)

    for key, fitness_list in all_results.items():
        if not fitness_list: continue
        min_fitness_in_key = min(fitness_list)
        if min_fitness_in_key < best_overall_fitness:
            best_overall_fitness = min_fitness_in_key
            best_overall_tour = best_tours[key]
            best_overall_key = key

    print(f"\nBeste gefundene Tour stammt von '{best_overall_key}' mit einer Länge von {best_overall_fitness:.2f}")

    plt.title(f'Beste gefundene Tour für {data_type.value} ({best_overall_key})', fontsize=16, weight='bold')
    # Städte plotten
    plt.scatter(coords[:, 0], coords[:, 1], c='red', zorder=2, label='Städte')

    # Tour plotten
    if best_overall_tour:
        # Schließe die Tour für die Visualisierung
        plot_tour = best_overall_tour + [best_overall_tour[0]]
        tour_coords = coords[plot_tour]
        plt.plot(tour_coords[:, 0], tour_coords[:, 1], 'b-', zorder=1, label='Beste Route')
    else:
        print("Keine gültige Tour zur Visualisierung gefunden.")

    plt.xlabel('X-Koordinate')
    plt.ylabel('Y-Koordinate')
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
    plt.show()
