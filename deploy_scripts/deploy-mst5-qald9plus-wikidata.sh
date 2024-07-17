#!/bin/bash
set -eu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
# activate python environment
source $PARENT_DIR/mst5-venv/bin/activate

# start the server
nohup python $PARENT_DIR/deploy_model.py \
    --model $PARENT_DIR/fine-tuned-models/qald9plus-finetune_lcquad2-ft-base_lc-ent \
    --knowledge_graph Wikidata \
    --linguistic_context \
    --entity_knowledge \
    --question_padding_length 128 \
    --entity_padding_length 64 \
    --port 8181 \
    --log_file $PARENT_DIR/logs/server-mst5-qald9plus-wiki.log > $PARENT_DIR/mst5-qald9plus-wikidata 2>&1 &