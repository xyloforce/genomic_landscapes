#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Class gene python for project M1 2020
# version 0.1
##########################################################

# TODO: à implémenter

class Gene():
    """This Gene class represent a gene in this pipeline."""

    def __init__(self, name, taxid, ncbiId, orthodbId):
        self.name = name
        self.taxid = taxid
        self.ncbiId = ncbiId
        self.orthodbId = orthodbId
        self.orthologs = []
        self.metric = dict()
