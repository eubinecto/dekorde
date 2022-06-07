# --- for building artifacts --- #
tokenizer:
	python3 main_build_tokenizer.py

kor2eng:
	python3 main_build_kor2eng.py

train:
	python3 main_train.py \
	--max_epochs=1000 \
	--batch_size=128 \
    --save_on_train_epoch_end=1 \
    --every_n_epochs=1 \
    --log_every_n_steps=2 \
    --check_val_every_n_epoch=1 \

train_overfit:
	python3 main_train.py \
    --overfit_batches=3 \
	--max_epochs=1000 \
	--batch_size=3 \
    --save_on_train_epoch_end=1 \
    --every_n_epochs=1 \
    --log_every_n_steps=3 \
    --check_val_every_n_epoch=1


train_check:
	python3 main_train.py \
	--fast_dev_run \
	--detect_anomaly \
	--max_epochs=1000 \
	--batch_size=3 \
    --save_on_train_epoch_end=1 \
    --every_n_epochs=1 \
    --log_every_n_steps=3 \
    --check_val_every_n_epoch=1


test:
	python3 main_test.py \
    --batch_size=64


test_check:
	python3 main_test.py \
	--fast_dev_run \
    --batch_size=3


streamlit:
	streamlit run main_streamlit.py