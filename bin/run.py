#!/usr/bin/env python

import sys
import argparse

from models import *

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-model', type=str, default=None, help='Model')
    parser.add_argument('-model-params', type=str, default=None, help='Model params')

    parser.add_argument('-train', action='store_true', help='Run training')
    parser.add_argument('-train_file', type=str, default=Model.default_train_file,
                        help='Pickle file for input training set dictionary')
    
    parser.add_argument('-test', action='store_true', help='Run testing')
    parser.add_argument('-test_file', type=str, default=Model.default_test_file,
                        help='Pickle file for input training set dictionary')

    parser.add_argument('-predict', action='store_true', help='Run prediction')
    parser.add_argument('-predict-in-file', type=str,
                        help='Pickle file for input prediction set dictionary')
    parser.add_argument('-predict-out-file', type=str,
                        help='Pickle file for input prediction set dictionary')

    parser.add_argument('-model-param', type=str, default=Model.default_model_param_file,
                        help='Pickle file for model parameters')

    args = parser.parse_args()

    if not isinstance(args.model, str):
        sys.exit('Model must be specified using -model')

    if not args.train and not args.test and not args.predict:
        sys.exit('One of -train/-test/-predict must be specified')
        
    return args

def main():
    args = parse_args()

    expr = ('{model_name}('
            'train_file="{train_file}", '
            'test_file="{test_file}", '
            'predict_in_file="{predict_in_file}", '
            'predict_out_file="{predict_out_file}", '
            'model_param_file="{model_param_file}"'
            '{other_params}'
            ')').format(model_name=args.model,
                        train_file=args.train_file, test_file=args.test_file,
                        predict_in_file=args.predict_in_file, predict_out_file=args.predict_out_file,
                        model_param_file=args.model_param,
                        other_params=(', ' + args.model_params) if args.model_params is not None else '')
    print 'Model =', expr

    if args.train:
        model = eval(expr, globals(), locals())
        model.train()
        model.save()

    if args.test:
        model = eval(expr, globals(), locals())
        model.load()
        model.test()
        
    if args.predict:
        model = eval(expr, globals(), locals())
        model.load()
        model.predict()
        
        
if __name__ == '__main__':
    main()
