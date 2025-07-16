from numpy.typing import NDArray
import numpy as np
from enum import Enum
import os
import json
import pandas as pd
import copy
KROA100_OPTIMUM = 21282
BERLIN52_OPTIMUM = 7542

class DataType(Enum):
    KROA100 = "kroA 100"
    BERLIN52 = 'Berlin 52'

DATA_2_OPTIMUM_TOUR = {DataType.KROA100: KROA100_OPTIMUM,
                       DataType.BERLIN52: BERLIN52_OPTIMUM}

def parse_tsp_data(data:str)->NDArray:
    """Parst die Koordinaten aus den TSP-Daten."""
    "data is a huge string for now"
    coords = []
    in_coord_section = False
    for line in data.splitlines():
        if "NODE_COORD_SECTION" in line:
            in_coord_section = True
            continue
        if "EOF" in line:
            break
        if in_coord_section and line.strip():
            parts = line.strip().split()
            if len(parts) == 3:
                coords.append((float(parts[1]), float(parts[2])))
    return np.array(coords)



def get_distance_matrix(coords:NDArray)->NDArray:
    """Erstellt eine Distanzmatrix aus den Koordinaten."""
    num_cities = len(coords) # n_rows for 2D array
    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i, num_cities):
            dist = np.linalg.norm(coords[i] - coords[j])
            dist_matrix[i, j] = dist_matrix[j, i] = dist
    return dist_matrix




def save_json(all_results, all_logs: dict[str, list[pd.DataFrame]], best_tours, save_name: str):
    corrected_all_logs = all_logs.copy()
    for key, data_frame_list in all_logs.items():
        for i, data_frame in enumerate(data_frame_list):
            corrected_all_logs[key][i] = data_frame.to_dict(orient='records')

    json_dict = {'all_results': all_results,
                 'all_logs': corrected_all_logs,
                 'best_tours': best_tours
                 }

    json_obj = json.dumps(json_dict, indent=8)

    if not os.path.exists("./output"):
        os.mkdir("./output")

    with open(f'./output/{save_name}.json', 'w') as f:
        f.write(json_obj)


def load_json(json_path):
    with open(json_path, 'r') as f:
        res = json.load(f)
        return res


def load_results(json_path):
    json_dict = load_json(json_path)
    all_results = json_dict['all_results']
    all_logs = json_dict['all_logs'].copy()
    best_tours = json_dict['best_tours']

    for key, list_of_dict_objs in json_dict['all_logs'].items():
        list_of_dataframes = list_of_dict_objs.copy()
        for i, to_be_df in enumerate(list_of_dict_objs):
            list_of_dataframes[i] = pd.DataFrame(to_be_df)
        all_logs[key] = list_of_dataframes
    return all_results, all_logs, best_tours


# --- KORREKTUR: Daten direkt einbetten, um Netzwerkfehler zu vermeiden ---
# Der Download von externen Quellen war unzuverlässig. Die Daten sind jetzt
# direkt im Code als String hinterlegt.

KROA100_data_string = """
NAME: kroA100
TYPE: TSP
COMMENT: 100-city problem A (Krolak/Felts/Nelson)
DIMENSION: 100
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
1 1380 939
2 2848 96
3 3510 1671
4 457 334
5 3888 666
6 984 965
7 2721 1482
8 1286 525
9 2716 1432
10 738 1325
11 1251 1832
12 2728 1698
13 3815 169
14 3683 1533
15 1247 1945
16 123 862
17 1234 1946
18 252 1240
19 611 673
20 2576 1676
21 928 1700
22 53 857
23 1807 1711
24 274 1420
25 2574 946
26 178 24
27 2678 1825
28 1795 962
29 3384 1498
30 3520 1079
31 1256 61
32 1424 1728
33 3913 192
34 3085 1528
35 2573 1969
36 463 1670
37 3875 598
38 298 1513
39 3479 821
40 2542 236
41 3955 1743
42 1323 280
43 3447 1830
44 2936 337
45 1621 1830
46 3373 1646
47 1393 1368
48 3874 1318
49 938 955
50 3022 474
51 2482 1183
52 3854 923
53 376 825
54 2519 135
55 2945 1622
56 953 268
57 2628 1479
58 2097 981
59 890 1846
60 2139 1806
61 2421 1007
62 2290 1810
63 1115 1052
64 2588 302
65 327 265
66 241 341
67 1917 687
68 2991 792
69 2573 599
70 19 674
71 3911 1673
72 872 1559
73 2863 558
74 929 1766
75 839 620
76 3893 102
77 2178 1619
78 3822 899
79 378 1048
80 1178 100
81 2599 901
82 3416 143
83 2961 1605
84 611 1384
85 3113 885
86 2597 1830
87 2586 1286
88 161 906
89 1429 134
90 742 1025
91 1625 1651
92 1187 706
93 1787 1009
94 22 987
95 3640 43
96 3756 882
97 776 392
98 1724 1642
99 198 1810
100 3950 1558
EOF
"""

# link = "https://github.com/mastqe/tsplib/blob/master/kroA100.tsp"


BERLIN52_data_string = """
NAME: berlin52
TYPE: TSP
COMMENT: 52 locations in Berlin (Groetschel)
DIMENSION: 52
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 565.0 575.0
2 25.0 185.0
3 345.0 750.0
4 945.0 685.0
5 845.0 655.0
6 880.0 660.0
7 25.0 230.0
8 525.0 1000.0
9 580.0 1175.0
10 650.0 1130.0
11 1605.0 620.0 
12 1220.0 580.0
13 1465.0 200.0
14 1530.0 5.0
15 845.0 680.0
16 725.0 370.0
17 145.0 665.0
18 415.0 635.0
19 510.0 875.0  
20 560.0 365.0
21 300.0 465.0
22 520.0 585.0
23 480.0 415.0
24 835.0 625.0
25 975.0 580.0
26 1215.0 245.0
27 1320.0 315.0
28 1250.0 400.0
29 660.0 180.0
30 410.0 250.0
31 420.0 555.0
32 575.0 665.0
33 1150.0 1160.0
34 700.0 580.0
35 685.0 595.0
36 685.0 610.0
37 770.0 610.0
38 795.0 645.0
39 720.0 635.0
40 760.0 650.0
41 475.0 960.0
42 95.0 260.0
43 875.0 920.0
44 700.0 500.0
45 555.0 815.0
46 830.0 485.0
47 1170.0 65.0
48 830.0 610.0
49 605.0 625.0
50 595.0 360.0
51 1340.0 725.0
52 1740.0 245.0
EOF
"""


DATA_TYPE_2_DATA_STRING = {DataType.KROA100: KROA100_data_string,
                       DataType.BERLIN52: BERLIN52_data_string}