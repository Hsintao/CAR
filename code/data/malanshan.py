#!/usr/bin/env python
# coding: utf-8
# ===================================
# @File    : malanshan.py
# @Time    : 2020/5/21
# @Author  : Xintao
# ===================================


import os
import glob
from data import srdata


class MALANSHAN(srdata.SRData):
    def __init__(self, args, name='MALANSHAN', train=True, benchmark=False):
        data_range = [r.split('-') for r in args.data_range.split('/')]
        if train:
            data_range = data_range[0]
        else:
            if args.test_only and len(data_range) == 1:
                data_range = data_range[0]
            else:
                data_range = data_range[1]

        self.begin, self.end = list(map(lambda x: int(x), data_range))
        super(MALANSHAN, self).__init__(
            args, name=name, train=train, benchmark=benchmark
        )

    def _scan(self):
        # names_hr, names_lr = super(MALANSHAN, self)._scan()
        # names_hr = names_hr[self.begin - 1:self.end]
        # names_lr = [n[self.begin - 1:self.end] for n in names_lr]

        train_damage_path = os.path.join(self.apath, 'train_damage_imgs')
        train_damage_imgs_path = sorted(glob.glob(os.path.join(train_damage_path, '*', '00*.png')))
        train_ref_imgs_path = [i.replace('damage', 'ref') for i in train_damage_imgs_path]

        val_damage_path = os.path.join(self.apath, 'val_damage_imgs')
        val_damage_imgs_path = sorted(glob.glob(os.path.join(val_damage_path, '*', '00*.png')))
        val_ref_imgs_path = [i.replace('damage', 'ref') for i in val_damage_imgs_path]
        if self.train:
            return train_ref_imgs_path, [train_damage_imgs_path]
        else:
            return val_ref_imgs_path, [val_damage_imgs_path]
        # val2train_num = int(len(val_damage_imgs_path) * 0.8) # 80%的验证集数据 加入到训练集中
        # if self.train:
        #     return train_ref_imgs_path + val_ref_imgs_path[:val2train_num], \
        #            [train_damage_imgs_path + val_damage_imgs_path[:val2train_num]]
        # else:
        #     return val_ref_imgs_path[val2train_num:], [val_damage_imgs_path[val2train_num:]]

    def _set_filesystem(self, dir_data):
        # super(MALANSHAN, self)._set_filesystem(dir_data)
        # self.dir_hr = os.path.join(self.apath, 'DIV2K_train_HR')
        # self.dir_lr = os.path.join(self.apath, 'DIV2K_train_LR_bicubic')
        # if self.input_large:
        #     self.dir_lr += 'L'
        self.apath = os.path.join(dir_data, self.name)
        self.ext = ('.png', '.jpg')
