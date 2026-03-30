#!/usr/bin/env python3

import argparse, os, pandas as pd, pysam


def extract_subseq_from_bam(bam, loci):
    # loci = 'chr2:176188810-176188810'
    chr_x, st, ed = loci.split(':')[0], int(loci.split(':')[1].split('-')[0]), int(loci.split(':')[1].split('-')[1])
    st = st-1
    # bam = '/mnt/nas1/lixq/project/PMseq/data_202507/bwaALT/S2015.srt.rmdup.bam'
    rangeA, rangeB = ed-6, ed+5
    print('Target:', chr_x, st, ed, (rangeA, rangeB))
    with pysam.AlignmentFile(bam) as bf:
        for read in (bf.fetch(chr_x, st, ed)):
            qid = read.query_name
            seq_pos = read.reference_start
            seq_st = read.reference_start
            seq_ed = read.reference_end
            seq_length = read.query_length
            seq = read.query_sequence
            MQ = read.mapping_quality
            if MQ == 0: continue
            relat_pos = 0
            cigartuples = read.cigartuples
            seq_x = ['N'] * 11
            for (operation, length) in cigartuples:
                lenadj = length if operation!=1 else 0
                if seq_pos < rangeA and seq_pos+lenadj> rangeB:
                    if operation in (0,7,8): seq_x = seq[relat_pos+(rangeA-seq_pos): relat_pos+(rangeB-seq_pos)]
                    elif operation in (2, ): seq_x = ['-'] * 11
                elif seq_pos < rangeA and seq_pos+lenadj> rangeA:
                    if operation in (0,7,8): seq_x[:seq_pos+lenadj-rangeA] = seq[relat_pos+(rangeA-seq_pos): relat_pos+lenadj]
                    elif operation in (2, ): seq_x[:seq_pos+lenadj-rangeA] = ['-'] * (seq_pos+lenadj-rangeA)
                elif seq_pos < rangeB and seq_pos+lenadj > rangeB:
                    if operation in (0,7,8): seq_x[-(rangeB-seq_pos):] = seq[relat_pos: relat_pos+(rangeB-seq_pos)]
                    elif operation in (2, ): seq_x[-(rangeB-seq_pos):] = ['-'] * (rangeB-seq_pos)
                elif seq_pos > rangeA and seq_pos+lenadj < rangeB:
                    if operation in (0,7,8): seq_x[seq_pos-rangeA:(seq_pos+lenadj)-rangeA] = seq[relat_pos: relat_pos+(lenadj)]
                    elif operation in (2, ): seq_x[seq_pos-rangeA:(seq_pos+lenadj)-rangeA] = ['-'] * lenadj
                    elif operation in (1, ): seq_x = seq_x[:seq_pos-rangeA] + list(seq[relat_pos: relat_pos+(lenadj)]) + seq_x[seq_pos-rangeA:]
                if operation not in (2,5): relat_pos += length
                if operation not in (1,4,5): seq_pos += length
            if seq_ed != seq_pos: print('Err pos',seq_ed, seq_pos); break
            if relat_pos != seq_length: print('Err len',seq_length, relat_pos); break
            print(qid, MQ, ''.join(seq_x), cigartuples, (seq_st, seq_ed))

def main(args):
    extract_subseq_from_bam(args.bam, args.loci)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Makefile for generate Block")
    parser.add_argument('-i', '--bam', required=True, type=str, dest='bam', help='<str> Block CSV file.')
    parser.add_argument('-l', '--loci', required=True, type=str, dest='loci', help='<str> Loci to extract.')
    # parser.add_argument('-o', '--out_prefix', required=False, type=str, default='.cov.csv', dest='outfile', help='<str> Prefix of output files.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = (parser.parse_args())
    print(args)
    main(args)