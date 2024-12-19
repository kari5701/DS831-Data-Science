import dash_ag_grid as dag
import pandas as pd
import pathlib

# Load the dataset
csv_path = pathlib.Path("data/html_cleaned.csv")
cleaned_data = pd.read_csv(csv_path)

# Define column definitions based on your dataset
columnDefs = [
    {'field': 'Title', 'headerName': 'Song Title'},
    {'field': 'Artist(s)', 'headerName': 'Artists'},
    {'field': 'Release Date', 'headerName': 'Release Date'},
    {'field': 'Genres', 'headerName': 'Genres'},
    {'field': 'Length', 'headerName': 'Song Length'},
    {'field': 'Label', 'headerName': 'Label'},
    {'field': 'Songwriters', 'headerName': 'Songwriters'},
    {'field': 'Producers', 'headerName': 'Producers'},
]
# Function to create a grid layout
def create_grid(data):
    grid = dag.AgGrid(
        style={"height": 800},
        id="getting-started-sort",
        rowData=data.to_dict("records"),
        columnDefs=columnDefs,
        columnSize="sizeToFit",
        defaultColDef={
            "filter": True,
            "floatingFilter": True,
            "sortable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True,
            "initialWidth": True,
            "resizable": True,
            },
        dashGridOptions={'animateRows': False,
                         'pagination': True,
                         'paginationPageSize': 18
        },
    )
    return grid
