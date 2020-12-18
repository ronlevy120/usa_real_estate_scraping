import argparse


class ArgParseInput:

    @staticmethod
    def argp():
        """Define the input variable which can be modified bia CLI"""
        parser = argparse.ArgumentParser(description="USA Real estate scraping arguments description:")

        parser.add_argument('places', const='new-york', nargs='?',  type=str, default='new-york',
                            help="Places in the US (city or states) to look for, enter with space between each place."
                                 " \nDefault: new-york")

        parser.add_argument('rows', type=int, const=9999, nargs='?', default=9999,
                            help="limit the number of pages of houses scraping results (~40 houses per page)")

        parser.add_argument('years', type=int, nargs='?', default=0,
                            help="presents the US real estate main stocks performance chart for the last N years")

        parser.add_argument('restart_data',const='do-not-restart', type=str, nargs='?', default="do-not-restart",
                            choices=['restart', 'do-not-restart'],
                                help="Choose whether to delete old observations or not")

        args = parser.parse_args()
        return list(map(lambda x: x.lower(), args.places.split(' '))), args.rows, args.years, args.restart_data
