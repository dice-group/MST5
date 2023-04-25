import urllib.request
import pandas as pd
import argparse


def get_html_data(id):
    fp = urllib.request.urlopen(
        "https://gerbil-qa.aksw.org/gerbil/experiment?id=" + id)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr


def get_results(html, output_file):
    html = pd.read_html(html)[0].rename(columns={
        "Unnamed: 3": "Benchmark"
    })
    html = html[html['Benchmark'].isna()]
    result = html.drop(
        columns=[
            'Dataset',
            'Language',
            'Error Count',
            'avg millis/doc',
            'Timestamp',
            'GERBIL version',
            'Benchmark'
        ]
    )
    result.to_csv(output_file, index=False)


def main():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="A program to extract lcqald questions and queries to csv dataset")

    # add arguments to the parser
    parser.add_argument("--id", type=str,
                        help="id of GERBIL experiment")
    parser.add_argument("-o", "--output", type=str,
                        help="name of output file")

    # parse the arguments
    args = parser.parse_args()
    gerbil_html = get_html_data(args.id)
    get_results(gerbil_html, args.output)


# check if this module is the main program
if __name__ == "__main__":
    # call the main function
    main()
