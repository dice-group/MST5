#!/bin/bash
set -eu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
# activate python environment
source $PARENT_DIR/mst5-venv/bin/activate

# start the server
nohup python $PARENT_DIR/deploy_model.py \
    --model $PARENT_DIR/fine-tuned-models/qald9plus-finetune_lcquad1-ft-base_lc-ent \
    --knowledge_graph DBpedia \
    --linguistic_context \
    --entity_knowledge \
    --question_padding_length 128 \
    --entity_padding_length 64 \
    --port 8185 \
    --log_file $PARENT_DIR/logs/server-mst5-qald9plus-dbp.log > $PARENT_DIR/mst5-qald9plus-dbpedia 2>&1 &