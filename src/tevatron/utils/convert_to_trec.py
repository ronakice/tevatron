"""Script to convert Tevatron predictions into TREC runs"""
import argparse
import collections
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Convert Tevatron predictions into TREC runs.')
parser.add_argument('--predictions_path', required=True,
                    help='Tevatron predictions file')
parser.add_argument('--output_path', required=True, help='output file')
parser.add_argument('--max_docs_run', type=int, default=1000,
                    help='number of hits to write to the run file.')

args = parser.parse_args()
examples = collections.defaultdict(dict)
# Merge all passage scores into a list of scores
with open(args.predictions_path) as f_pred:
    for line_pred in f_pred:
        query_id, doc_id, score = line_pred.strip().split()
        if query_id == doc_id:
            continue
        examples[query_id][doc_id] = score



with open(args.output_path, 'w') as fout:
    for query_id, doc_ids_scores in tqdm(examples.items()):
        doc_ids_scores = [(doc_id, scores)
            for doc_id, scores in doc_ids_scores.items()]
        doc_ids_scores.sort(key=lambda x: x[1], reverse=True)
        rank = 1
        for doc_id, score in doc_ids_scores:
            if rank <= args.max_docs_run:
                fout.write(
                    f'{query_id} Q0 {doc_id} {rank} {score} tevatron\n')
            rank += 1