import matplotlib.pyplot as plt
import numpy as np

def plot_macro_f1(languages: set, f1_scores: dict, x_distance, figsize):
    x = np.arange(len(languages)) * x_distance  # the label locations
    width = 0.4  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained', figsize=figsize)

    for attribute, measurement in f1_scores.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, fmt='%.2f')
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1 Score')
    ax.set_title('F1 Scores by languages')
    ax.set_xticks(x + width*(len(f1_scores)-1)/2, languages)
    ax.legend(loc='upper left', ncols=3)
    plt.show()


def get_lang_set(results):
    languages_list = [set(result["Language"].tolist())
                      for result in results.values()]
    return set().union(*languages_list)


def get_f1_scores(results, languages):
    f1_scores = {}
    for name, result_df in results.items():
        scores = list()
        for lang in languages:
            try:
                macro_f1 = result_df.loc[result_df["Language"]
                                         == lang, "Macro F1"].iloc[0]
            except:
                macro_f1 = 0
            scores.append(macro_f1)
        f1_scores[name] = scores
    return f1_scores

def plot(results, x_distance=1, figsize=(8, 8)):
    languages = get_lang_set(results)
    f1_scores = get_f1_scores(results, languages)
    plot_macro_f1(languages, f1_scores, x_distance, figsize)