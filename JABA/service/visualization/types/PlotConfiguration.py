class PlotConfiguration:

    name = ""
    
    initial_frame = None
    final_frame = None

    map_list = []

    variable_type = None

    index, data = None, None

    def __init__(self, name, initial_frame, final_frame, map_list, variable_type,
                 index, data):
        self.name = name
        self.initial_frame = initial_frame
        self.final_frame = final_frame
        self.map_list = map_list
        self.variable_type = variable_type

        self.index = index
        self.data = data
