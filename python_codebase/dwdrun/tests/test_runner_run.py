import argparse
import datetime


def main(args):
    print("DD 123 - test runner has worked.{args.jobModule} {args.runDate}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arg parsing example")
    parser.add_argument("jobModule", default="data_aquisition.market_data.ecb.fx_api")
    parser.add_argument("runDate", default=datetime.date(2024, 1, 1))
    args = parser.parse_args()
    main(args)
