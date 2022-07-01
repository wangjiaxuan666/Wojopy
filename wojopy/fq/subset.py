import os
import pysam
import re


def sub_pair_fq(file1, file2, pattern):
    """Extract the paired read from the PE platfrom reads
    :param file1: the read1 file
    :param file2: the read2 file
    :param pattern: the python re module regrex expression which distinguish two read file like @read29299[.1] and
    @read29299[.2], then the paremeter should be '\.[1-2]$',the default value is noting to replace
    :return: the fq files
    """
    if pattern is None:
        pattern = ""
    with pysam.FastxFile(file1) as read1:
        read1_set = {}
        for entry in read1:
            seqid = re.sub(pattern, "", entry.name)
            read1_set[seqid] = [entry.comment, entry.quality.strip(), entry.sequence.strip()]
    with pysam.FastxFile(file2) as read2:
        read2_set = {}
        for entry in read2:
            seqid = re.sub(pattern, "", entry.name)
            read2_set[seqid] = [entry.comment, entry.quality.strip(), entry.sequence.strip()]
    read1_up_list = set(read1_set) - set(read2_set)
    read2_up_list = set(read2_set) - set(read1_set)
    read_p_list = set(read1_set) & set(read2_set)
    if entry.quality is not None:
        suffix = "fq"
    else:
        suffix = "fa"
    read1_p = open("{}.paired.{}".format(
        os.path.basename(file1).replace(".gz", "").replace(".fq", "").replace("fastq", "").replace("fasta", "").replace(
            ".fa", ""), suffix), "w")
    read2_p = open("{}.paired.{}".format(
        os.path.basename(file2).replace(".gz", "").replace(".fq", "").replace("fastq", "").replace("fasta", "").replace(
            ".fa", ""), suffix), "w")
    read1_u = open("{}.unpaired.{}".format(
        os.path.basename(file1).replace(".gz", "").replace(".fq", "").replace("fastq", "").replace("fasta", "").replace(
            ".fa", ""), suffix), "w")
    read2_u = open("{}.unpaired.{}".format(
        os.path.basename(file2).replace(".gz", "").replace(".fq", "").replace("fastq", "").replace("fasta", "").replace(
            ".fa", ""), suffix), "w")
    for seq_id in read_p_list:
        seq_comment, seq_quality, seq_sequence = read1_set[seq_id]
        if seq_comment is None:
            read1_p.write("@" + seq_id + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
        else:
            read1_p.write(
                "@" + seq_id + " " + seq_comment + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
        seq_comment, seq_quality, seq_sequence = read2_set[seq_id]
        if seq_comment is None:
            read2_p.write("@" + seq_id + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
        else:
            read2_p.write(
                "@" + seq_id + " " + seq_comment + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
    for seq_id in read1_up_list:
        seq_comment, seq_quality, seq_sequence = read1_set[seq_id]
        if seq_comment is None:
            read1_u.write("@" + seq_id + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
        else:
            read1_u.write(
                "@" + seq_id + " " + seq_comment + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
    for seq_id in read2_up_list:
        seq_comment, seq_quality, seq_sequence = read2_set[seq_id]
        if seq_comment is None:
            read2_u.write("@" + seq_id + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
        else:
            read2_u.write(
                "@" + seq_id + " " + seq_comment + "\n" + seq_sequence + "\n" + "+" + "\n" + seq_quality + "\n")
    read1_p.close()
    read2_p.close()
    read1_u.close()
    read2_u.close()
