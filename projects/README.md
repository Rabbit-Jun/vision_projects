## Project

- 음성 데이터를 이용한 Connectionist Temporal Classification (CTC) 기반 음성 인식 모델
- input : 음성 데이터 파일(.wav)


## Folder Structure

```
project
├── data
│ 
├── src
│ └── paranoma.py 
│ └── special_effect.py
│
├── environment.yml
└── poetry.lock
│
├── pyproject.toml
└── README.md
```

## Environment

- Anaconda Powerell Prompt

## conda에서 라이브러리 설치 방법
```
conda env create -f environment.yml
```
## poetry에서 라이브러리 설치 방법
```
poetry install
``` 


## 코드 실행

project에서 
```
python src/paranoma.py
python src/special_effect.py
```