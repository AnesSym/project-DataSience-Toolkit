
import matplotlib.pyplot as plt
import pandas as pd

def plot_(x = None, 
          y = None, 
          graph_type = None, 
          label_x = None, 
          label_y = None, 
          colors = None, 
          figure_size = (10,6), 
          title = None, 
          separate = False, 
          grid = False, 
          bins = 10):
    """The function creates a plot based on the specified parameters and returns the plot object.
    Args:
        x (float): array-like object containing x-coordinates of data points to be plotted. Defaults to None.
        y (float): array-like object containing y-coordinates of data points to be plotted. Defaults to None.
        graph_type (str, list): a string or a list of strings representing the type of plot to be created. Defaults to None.
        label_x (str): a string representing the label for the x-axis. Defaults to None.
        label_y (str): a string representing the label for the y-axis. Defaults to None.
        colors (str): a string or a list of strings representing the colors of the plot elements. Default is None.
        figure_size (tuple): a tuple representing the dimensions of the plot figure. Defaults to (10,6).
        title (str): a string representing the title of the plot. Defaults to None.
        separate (bool): a boolean value representing whether to separate multiple histograms or not. Defaults to False.
        grid (bool): a boolean value representing whether to show the grid or not. Default is False. Defaults to False.
        bins (int): an integer representing the number of bins in the histogram. Defaults to 10.

    Raises:
        ValueError: graph_type must be a string or a list of strings
        ValueError: Invalid graph_type. Try: scatter, bar, hist, line, hist2d
    Returns:
        object: plot object
    """
    plt.style.use('_mpl-gallery')
    if isinstance([graph_type, colors], str):
        graph_type, colors = [graph_type], [colors]
    elif not isinstance([graph_type, colors], list):
        raise ValueError("graph_type must be a string or a list of strings")
    
    def plot_type (entry):
            graph_list_scalar = graph_list.iloc[0] if isinstance(graph_list, pd.Series) else graph_list
            if graph_list_scalar == "scatter":
                return plt.scatter(x,y, color = colors) 
            elif graph_list_scalar== "line" or graph_list == None:
                return plt.plot(x,y, color = colors)
            elif graph_list_scalar == "stackplot":
                return plt.stackplot(x, y, color = colors)
            elif graph_list_scalar == "bar":
                return plt.bar(x,y, color = colors)
            elif graph_list_scalar == "hist": 
                if x is None:
                    return plt.hist(y, bins = bins, color = colors)
                elif y is None:
                    return plt.hist(x, bins = bins, color = colors)
                elif separate:
                    return plt.hist(x, bins = bins, color = colors), plt.gca().set(title=title, xlabel=label_x, ylabel=label_y),plt.grid(grid),plt.show(),plt.figure(figsize=figure_size),plt.hist(y, bins = bins, color= colors)
                else:
                    return plt.hist(x, bins = bins, color = colors), plt.hist(y, bins = bins)
            elif graph_list_scalar == "hist2d":
                return plt.hist2d(x, y, bins = bins, color = colors)
            else:
                raise ValueError("Invalid graph_type. Try: scatter, bar, hist, line, hist2d")
    
    for graph_list in graph_type:
        graph_list = graph_list.lower()
        plt.figure(figsize = figure_size)
        plot_type(entry = graph_type)
        plt.gca().set(title = title, xlabel = label_x, ylabel = label_y)
        plt.grid(grid)
        plt.show()
    


 

