# 데이터 전처리 실행 예
> cd melo
> python preprocess_text.py --metadata data/kss/metadata.list --config_path data/kss/config.json
> python preprocess_text.py --metadata data/f-h3-d-005/metadata.list --config_path data/f-h3-d-005/config.json
> python preprocess_text.py --metadata data/F-A2-B-021-0101/metadata.list --config_path data/F-A2-B-021-0101/config.json --val-per-spk 8
> python preprocess_text.py --metadata data/K-H1-B-064/metadata.list --config_path data/K-H1-B-064/config.json --val-per-spk 8

# 학습 스크립트 실행 예
> cd melo
> bash train_ko.sh data/kss/config.json 2
> bash train_ko.sh data/f-h3-d-005/config.json 2
> bash train_ko.sh data/F-A2-B-021-0101/config.json 2
> bash train_ko.sh data/K-H1-B-064/config.json 2
