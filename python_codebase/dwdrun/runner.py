import datetime
import argparse
import importlib

def main(args):
    arg_module = args.module
    arg_module_import = importlib.import_module(arg_module)
    arg_module_import.main(args)

    # Your code to use the runtime argument goes here

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse arguments for runtime.')
    parser.add_argument("module", default="data_aquisition.market_data.ecb.fx_api")
    parser.add_argument("run_date", default=datetime.date(2024,1,1))
    parser.add_argument('--file', type=str, help='Specify the runtime for the file.')
    args = parser.parse_args()
    main(args)