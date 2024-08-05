#!/bin/bash

if [ $# -ne 3 ]; then
    echo "사용법: $0 <language> <model_path> <output_path>"
    exit 1
fi

LANGUAGE=$1
MODEL_PATH=$2
OUTPUT_PATH=$3

if [ ! -f run_test.txt ]; then
    echo "texts.txt 파일이 현재 디렉토리에 없습니다."
    exit 1
fi

# read test file
while IFS= read -r line || [ -n "$line" ]
do
    python infer.py --text "$line" -l "$LANGUAGE" -m "$MODEL_PATH" -o "$OUTPUT_PATH"
done < run_test.txt

echo "스크립트 실행 완료."