# notebooks/installation_instruction.ipynb
install: mst5-venv datasets/lcquad1
	mst5-venv/bin/pip install -r requirements.txt
	mst5-venv/bin/python -m spacy download zh_core_web_sm
	mst5-venv/bin/python -m spacy download en_core_web_sm
	mst5-venv/bin/python -m spacy download fr_core_news_sm
	mst5-venv/bin/python -m spacy download de_core_news_sm
	mst5-venv/bin/python -m spacy download ja_core_news_sm
	mst5-venv/bin/python -m spacy download lt_core_news_sm
	mst5-venv/bin/python -m spacy download ru_core_news_sm
	mst5-venv/bin/python -m spacy download es_core_news_sm
	mst5-venv/bin/python -m spacy download uk_core_news_sm
mst5-venv:
	python3 -m venv --system-site-packages mst5-venv
datasets/lcquad1:
	./download_datasets.sh
