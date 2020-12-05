import os, sys
import pandas as pd


def auto_fix(nodes_csv: str, rels_csv: str, cpg_edges_csv: str) -> None:
    assert os.path.exists(nodes_csv)
    assert os.path.exists(rels_csv)
    assert os.path.exists(cpg_edges_csv)
    print(f"""
nodes_csv       ::  {nodes_csv}
rels_csv        ::  {rels_csv}
cpg_edges_csv   ::  {cpg_edges_csv}
    """)
    cpg_edges = pd.read_csv(cpg_edges_csv, delimiter="\t", keep_default_na=False, )
    rels = pd.read_csv(rels_csv, delimiter="\t", keep_default_na=False, )
    nodes = pd.read_csv(nodes_csv, delimiter="\t", keep_default_na=False, escapechar='\\',)
    nodes.rename(columns={'id:int': 'id:ID', 'labels:label': 'LABEL', 'flags:string_array': 'flags:string[]'},
                 inplace=True)
    rels.rename(columns={'start': ':START_ID', 'end': ':END_ID', 'type': ':TYPE'}, inplace=True)
    cpg_edges.rename(columns={'start': ':START_ID', 'end': ':END_ID', 'type': ':TYPE'}, inplace=True)
    nodes.to_csv(nodes_csv, index=False)
    rels.to_csv(rels_csv, index=False)
    cpg_edges.to_csv(cpg_edges_csv, index=False)


assert sys.argv.__len__() == 4
auto_fix(nodes_csv=sys.argv[1], rels_csv=sys.argv[2], cpg_edges_csv=sys.argv[3])
