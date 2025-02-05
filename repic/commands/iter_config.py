#!/usr/local/bin/python3
#
#	iter_config.py -  sets general iterative ensemble particle picking parameters
#	author: Christopher JF Cameron
#

import copy
from repic.utils.common import *

name = "iter_config"
#   default Conda enviroment names for SPHIRE-crYOLO, DeepPicker, and Topaz
env_dict = {
    "cryolo": "cryolo",
    "deep": "deep",
    "topaz": "topaz"
}
#   expected DeepPicker files
exp_deep_files = set([
    "analysis_pick_results.py",
    "autoPicker.py",
    "autoPick.py",
    "dataLoader.py",
    "deepModel.py",
    "display.py",
    "extractData.py",
    "Makefile",
    "README.md",
    "starReader.py",
    "train.py",
    os.path.join("trained_model", "checkpoint"),
    os.path.join("trained_model", "model_demo_type3"),
    os.path.join("trained_model", "model_demo_type3.meta")
])


def add_arguments(parser):
    parser.add_argument(
        "data_dir", help="path to directory containing training data")
    parser.add_argument("box_size", type=int,
                        help="particle detection box size (in int[pixels])")
    parser.add_argument("exp_particles", type=int,
                        help="number of expected particles (int)")
    parser.add_argument(
        "cryolo_model", help="path to LOWPASS SPHIRE-crYOLO model")
    parser.add_argument("deep_dir", help="path to DeepPicker scripts")
    parser.add_argument("topaz_scale", type=int,
                        help="Topaz scale value (int)")
    parser.add_argument("topaz_rad", type=int,
                        help="Topaz particle radius size (in int[pixels])")
    parser.add_argument("--cryolo_env", type=str, default=env_dict['cryolo'],
                        help=f"Conda environment name for SPHIRE-crYOLO installation (default:{env_dict['cryolo']})")
    parser.add_argument("--deep_env", type=str, default=env_dict['deep'],
                        help=f"Conda environment name for DeepPicker installation (default:{env_dict['deep']})")
    parser.add_argument("--topaz_env", type=str, default=env_dict['topaz'],
                        help=f"Conda environment name for Topaz installation (default:{env_dict['topaz']})")
    parser.add_argument("--out_file_path", type=str, default="iter_config.json",
                        help="path for created config file (default:./iter_config.json)")


def main(args):

    print("Validating config parameters")
    #	check that the training data directory and SPHIRE-crYOLO model exist
    assert(os.path.exists(args.data_dir)
           ), f"Error - training data directory does not exist: {args.data_dir}"
    assert(os.path.exists(args.cryolo_model)
           ), f"Error - provided SPHIRE-crYOLO model not found: {args.crolo_model}"

    #   check that DeepPicker path is valid
    assert(os.path.exists(args.deep_dir)
           ), f"Error - DeepPicker directory does not exist: {args.deep_dir}"
    #   check that DeepPicker folder contains expected files
    prefix = os.path.join(args.deep_dir, '')
    deep_files = set([file.replace(os.path.join(prefix), '')
                      for file in glob.glob(os.path.join(prefix, "**", '*'), recursive=True)])
    deep_files = exp_deep_files - deep_files
    assert(len(deep_files) ==
           0), f"Error - DeepPicker file(s) are missing: {', '.join(deep_files)}"
    del prefix, deep_files

    #   check that provided Conda environment names can be found
    envs = []
    stdout = subprocess.check_output(
        "conda info --envs", shell=True).decode(sys.stdout.encoding).strip()
    for line in stdout.split('\n'):
        if line.startswith(('#', ' ')):
            continue
        envs.append(line.split()[0])
    envs = set([args.cryolo_env, args.deep_env, args.topaz_env]) - set(envs)
    assert(len(envs) ==
           0), f"Error - Conda environment(s) not found: {', '.join(envs)}"
    del envs, stdout, line

    #   write JSON file of iter_pick parameters
    print(f"Writing config file to {args.out_file_path}")
    params_dict = vars(copy.deepcopy(args))
    del params_dict["command"]
    del params_dict["out_file_path"]
    del params_dict["func"]
    with open(args.out_file_path, 'wt') as o:
        json.dump(params_dict, o, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    main(args)
