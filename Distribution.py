import sys
import os
import matplotlib.pyplot as plt


def main():
    if len(sys.argv) != 2:
        print("Usage: python Distribution.py <data_file>")
        sys.exit(1)

    data_folder = sys.argv[1]
    if not os.path.isdir(data_folder):
        print(f"Error: Directory '{data_folder}' not found.")
        sys.exit(1)

    data: dict[str, dict[str, int]] = read_data(data_folder)
    create_charts(data)


def read_data(data_folder) -> dict[str, dict[str, int]]:
    data: dict[str, dict[str, int]] = {
        category: {
            subfolder: len(os.listdir(os.path.join(data_folder,
                                                   category,
                                                   subfolder)))
            for subfolder in os.listdir(os.path.join(data_folder,
                                                     category))
        }
        for category in os.listdir(data_folder)
    }
    return data


def create_charts(data: dict[str, dict[str, int]]):
    for category, subfolders in data.items():
        colors = plt.cm.Set3.colors
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.pie(
            subfolders.values(),
            labels=subfolders.keys(),
            autopct='%1.1f%%',
            colors=colors
            )
        plt.title(f"Distribution of {category}")
        plt.subplot(1, 2, 2)
        plt.bar(
            subfolders.keys(),
            subfolders.values(),
            color=colors
            )
        plt.title(f"Histogram of {category}")
        plt.xlabel("Categories")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"1-Analysis/{category}_distribution.png")
        plt.show()
        plt.close()


if __name__ == "__main__":
    main()
