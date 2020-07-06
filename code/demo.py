#!/usr/bin/env python
# coding: utf-8
# ===================================
# @File    : demo.py
# @Time    : 2020/5/21
# @Author  : Xintao
# ===================================


import torch

import utility
import data
import model
import loss
from option import args
from trainer import Trainer

torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)


def main():
    global model
    args.cpu = True
    if args.data_test == ['video']:
        from videotester import VideoTester
        model = model.Model(args, checkpoint)
        print('total params: %.2fM' % (sum(p.numel()
                                           for p in model.parameters()) / 1000000.0))
        t = VideoTester(args, model, checkpoint)
        t.test()
    else:
        if checkpoint.ok:
            loader = data.Data(args)
            _model = model.Model(args, checkpoint)
            print('total params:%.2fM' % (sum(p.numel()
                                              for p in _model.parameters()) / 1000000.0))
            _loss = loss.Loss(args, checkpoint) if not args.test_only else None
            t = Trainer(args, loader, _model, _loss, checkpoint)
            while not t.terminate():
                t.train()
                t.test()

            checkpoint.done()


if __name__ == '__main__':
    main()
