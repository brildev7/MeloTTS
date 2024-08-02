# 데이터 전처리 실행 예
> cd melo
> python preprocess_text.py --metadata data/kss/metadata.list --config_path data/kss/config.json
> python preprocess_text.py --metadata data/f-h3-d-005/metadata.list --config_path data/f-h3-d-005/config.json

# 학습 스크립트 실행 예
> cd melo
> bash train_ko.sh data/kss/config.json 2
> bash train_ko.sh data/f-h3-d-005/config.json 2
