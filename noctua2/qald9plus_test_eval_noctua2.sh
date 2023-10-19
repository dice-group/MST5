#!/bin/bash

EVAL_SCRIPT=noctua2/noctua2_eval.sh
FT_ROOT=fine-tuned_models
TEST_NAME=q9p_test
TEST_FILE=datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json
OUTPUT_ROOT=predictions_qald9plus_test
LANGS="en"

### lcquad2-finetune_mt5-base ###
MODEL_NAMES=("lcquad2-finetune_mt5-base" "qald9plus-finetune_mt5-base" "qald9plus-finetune_lcquad2-ft-base")

# This loop only prints the formatted commands. It does not execute them.
for MODEL in "${MODEL_NAMES[@]}"
do
    echo "### Eval ${MODEL} ###"
    echo sbatch --job-name="eval_${MODEL}_simple" $EVAL_SCRIPT $FT_ROOT ${MODEL}_simple $TEST_FILE $OUTPUT_ROOT $LANGS false false
    echo sbatch --job-name="eval_${MODEL}_lc"  $EVAL_SCRIPT $FT_ROOT ${MODEL}_lc $TEST_FILE $OUTPUT_ROOT $LANGS true false
    echo sbatch --job-name="eval_${MODEL}_ent"  $EVAL_SCRIPT $FT_ROOT ${MODEL}_ent $TEST_FILE $OUTPUT_ROOT $LANGS false true
    echo sbatch --job-name="eval_${MODEL}_lc-ent"  $EVAL_SCRIPT $FT_ROOT ${MODEL}_lc-ent $TEST_FILE $OUTPUT_ROOT $LANGS true true
    echo "######"
done

: '
## Expected Output:

### Eval lcquad2-finetune_mt5-base ###
sbatch --job-name=eval_lcquad2-finetune_mt5-base_simple noctua2/noctua2_eval.sh fine-tuned_models lcquad2-finetune_mt5-base_simple datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false false
sbatch --job-name=eval_lcquad2-finetune_mt5-base_lc noctua2/noctua2_eval.sh fine-tuned_models lcquad2-finetune_mt5-base_lc datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true false
sbatch --job-name=eval_lcquad2-finetune_mt5-base_ent noctua2/noctua2_eval.sh fine-tuned_models lcquad2-finetune_mt5-base_ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false true
sbatch --job-name=eval_lcquad2-finetune_mt5-base_lc-ent noctua2/noctua2_eval.sh fine-tuned_models lcquad2-finetune_mt5-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true true
######
### Eval qald9plus-finetune_mt5-base ###
sbatch --job-name=eval_qald9plus-finetune_mt5-base_simple noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_mt5-base_simple datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false false
sbatch --job-name=eval_qald9plus-finetune_mt5-base_lc noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_mt5-base_lc datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true false
sbatch --job-name=eval_qald9plus-finetune_mt5-base_ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_mt5-base_ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false true
sbatch --job-name=eval_qald9plus-finetune_mt5-base_lc-ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_mt5-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true true
######
### Eval qald9plus-finetune_lcquad2-ft-base ###
sbatch --job-name=eval_qald9plus-finetune_lcquad2-ft-base_simple noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_simple datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false false
sbatch --job-name=eval_qald9plus-finetune_lcquad2-ft-base_lc noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true false
sbatch --job-name=eval_qald9plus-finetune_lcquad2-ft-base_ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en false true
sbatch --job-name=eval_qald9plus-finetune_lcquad2-ft-base_lc-ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test en true true
######

### QALD 9 Plus -Multilingual 

sbatch --time=12:00:00 --begin=now+2hour --job-name=eval_qald9plus-finetune_lcquad2-ft-base_lc-ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc-ent datasets/qald9plus/wikidata/qald_9_plus_test_wikidata.json predictions_qald9plus_test_multilingual "en,de,ru,fr,lt,ba,be,uk,zh,ja,es" true true

### QALD 10 - Multilingual

sbatch --time=15:00:00 --begin=now+2hour --job-name=eval_qald9plus-finetune_lcquad2-ft-base_lc-ent noctua2/noctua2_eval.sh fine-tuned_models qald9plus-finetune_lcquad2-ft-base_lc-ent datasets/qald10/qald_10.json predictions_qald10_multilingual "en,de,ru,zh,ja" true true

'