import argparse


class ArgParseInput:

    @staticmethod
    def argp():
        """Define the input variable which can be modified bia CLI"""
        parser = argparse.ArgumentParser(description="List of places to scrap")
        parser.add_argument('places', const='new-york', nargs='?',  type=str, default='new-york',
                            help="Places in the US to look for, space between each place. Default: new-york")
        parser.add_argument('rows', type=int, const=9999, nargs='?', default=9999,
                            help="limit the number of results you might receive")
        args = parser.parse_args()
        return list(map(lambda x: x.lower(), args.places.split(' '))), args.rows
