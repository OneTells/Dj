from matplotlib import pyplot as plt


class Drawer:

    @staticmethod
    def draw_vertical_histogram(title: str, data: dict, path: str, tick_size: int = 8, font_size: int = 12) -> None:
        plt.title(title, fontsize=font_size)

        plt.bar(list(data.keys()), list(data.values()))

        plt.grid(axis='y')
        plt.xticks(list(data.keys()), rotation='vertical', fontsize=tick_size)
        plt.tick_params(axis='y', labelsize=tick_size)

        plt.savefig(path)
        plt.close()

    @staticmethod
    def draw_horizontal_histogram(title: str, data: dict, path: str, tick_size: int = 8, font_size: int = 12):
        plt.title(title, fontsize=font_size)

        plt.barh(list(data.keys()), list(data.values()))
        plt.yticks(
            list(data.keys()), list(data.keys()), fontdict={'horizontalalignment': 'right', 'verticalalignment': 'center'}
        )

        plt.tick_params(axis='y', labelsize=tick_size - 2)
        plt.tick_params(axis='x', labelsize=tick_size)

        plt.grid(axis='x')
        plt.gca().invert_yaxis()

        plt.savefig(path)
        plt.close()

    @staticmethod
    def draw_pie(title: str, data: dict, path: str, text_size: int = 8, font_size: int = 12):
        plt.title(title, fontsize=font_size)

        plt.pie(list(data.values()), labels=list(data.keys()), textprops={'fontsize': text_size})
        plt.axis('equal')

        plt.savefig(path)
        plt.close()