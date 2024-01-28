import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.dates import date2num

def generate_scatter_plot(authors_dates):
    authors = list(set([touch['author'] for touches in authors_dates.values() for touch in touches]))
    colors = cm.rainbow([i / len(authors) for i in range(len(authors))])
    
    for i, (file_path, touches) in enumerate(authors_dates.items()):
        dates = [touch['date'] for touch in touches]
        weeks = [(date - min(dates)).days // 7 for date in dates]
        author_color = colors[authors.index(touches[0]['author'])]

        plt.scatter(weeks, [i] * len(dates), color=author_color, label=file_path)

    plt.xlabel('Weeks')
    plt.ylabel('Authors')
    plt.title('Weeks vs Authors for Touched Files')
    plt.legend()
    plt.show()

# Generate scatter plot
generate_scatter_plot(authors_dates)
