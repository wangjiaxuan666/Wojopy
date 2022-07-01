import os
import pandas as pd


def split_col_big(infile, idlist, split_str=None):
    if split_str is None:
        id_list = pd.read_csv(idlist, sep=",")
    else:
        id_list = pd.read_csv(idlist, sep=",")
        id_list = id_list.iloc[:, 0].str.split(split_str, expand=True)
    id_list['colnum'] = id_list.index + 2
    del id_list[1]
    colmin = id_list.groupby(0).min()
    colmax = id_list.groupby(0).max()
    id_loc = pd.merge(colmin, colmax, suffixes=("_min", "_max"), how='inner', left_index=True, right_index=True)
    id_loc.to_csv("123.csv")
    if not os.path.exists("split"):
        os.mkdir("split")
    with open(os.path.basename(idlist) + '_output.sh', 'w') as file:
        file.write(
            "#!/bin/bash \n#SBATCH -o job.%j.out\n#SBATCH -J UKB_split\n#SBATCH --nodes=1\n#SBATCH "
            "--ntasks-per-node=150\n")
        command = '''nohup awk -v FPAT='([^,]*)|("[^"]+")' -v OFS=',' '{print$1,%s}' %s > split/%s.csv & \n'''
        # command = '''awk -v FPAT="([^,]+)|(\"[^\"]+\")" -v OFS=',' '{print$1,%s}' %s > split/%s.csv'''
        for i in range(0, len(id_loc)):
            col = range(id_loc.iloc[i, 0], id_loc.iloc[i, 1] + 1)
            cols = ['$' + str(x) for x in col]
            file.write(command % (",".join(cols), infile, str(id_loc.index[i])))
        file.write("wait\n")

# head ukb52329.csv | awk 'NR==1{print$1}' > id.list
# cat id.list | sed "s:,:\n:ig" | sed 's/"//ig' > id.list1
