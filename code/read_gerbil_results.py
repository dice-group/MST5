import urllib.request
import pandas
import argparse
import csv

def get_html_data():
    fp = urllib.request.urlopen("https://gerbil-qa.aksw.org/gerbil/experiment?id=202304170000")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr

gerbil_html = get_html_data()

def get_results(html):
    html = pandas.read_html(html)[0].rename(columns={
    "Unnamed: 3": "Benchmark"
})
    html = html[html['Benchmark'].isna()]
    return html.drop(columns=['Dataset', 'Language', 'Error Count', 'avg millis/doc', 'Timestamp', 'GERBIL version', 'Benchmark'])

result_df = get_results(gerbil_html)
print(result_df)

def main():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A program to extract lcqald questions and queries to csv dataset")

    # add arguments to the parser
    parser.add_argument("knowledge_graph", choices=[
                        "wikidata", "dbpedia"], help="choose the knowledge graph", default="wikidata")
    parser.add_argument("-i", "--input", type=str, help="name of input file")
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file", default="lcqald.csv")

    # parse the arguments
    args = parser.parse_args()

# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()

