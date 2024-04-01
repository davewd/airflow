import argparse

def main(args):
    print("DD 123 - test runner has worked.")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arg parsing example")
    parser.add_argument("module", default="data_aquisition.market_data.ecb.fx_api")
    parser.add_argument("run_date", default=datetime.date(2024,1,1))
    parser.add_argument('--file', type=str, help='Specify the runtime for the file.')
    args = parser.parse_args()
    main(args)