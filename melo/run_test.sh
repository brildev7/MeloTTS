#!/bin/bash

# 스크립트 실행에 필요한 인자가 제공되었는지 확인
if [ $# -ne 3 ]; then
    echo "사용법: $0 <language> <model_path> <output_path>"
    exit 1
fi

LANGUAGE=$1
MODEL_PATH=$2
OUTPUT_PATH=$3

# texts.txt 파일이 동일한 디렉토리에 있는지 확인
if [ ! -f run_test.txt ]; then
    echo "texts.txt 파일이 현재 디렉토리에 없습니다."
    exit 1
fi

# texts.txt 파일 읽기
while IFS= read -r line || [ -n "$line" ]
do
    # 라인을 한번씩 infer.py 스크립트 실행
    python infer.py --text "$line" -l "$LANGUAGE" -m "$MODEL_PATH" -o "$OUTPUT_PATH"
done < run_test.txt

echo "스크립트 실행 완료."