
tokenizer:
	python3 main_build_tokenizer.py

kor2eng:
	python3 main_build_kor2eng.py

train:
	python3 main_train.py \
	--max_epochs=60 \
    --save_top_k=5 \
    --save_on_train_epoch_end=1 \
    --every_n_epochs=1 \
    --log_every_n_steps=2 \
    --check_val_every_n_epoch=1

eval:
	python3 main_eval.py \
    --max_epochs=1

# pseudo-tests
test_train:
	python3 main_train.py \
	--fast_dev_run \
	--max_epochs=60 \
    --save_top_k=5 \
    --save_on_train_epoch_end=1 \
    --every_n_epochs=1 \
    --log_every_n_steps=2 \
    --check_val_every_n_epoch=1

test_eval:
	python3 main_eval.py --fast_dev_run