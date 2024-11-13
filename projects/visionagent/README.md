## Project

- 내용
- 


## Folder Structure

```
visionagent
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

- `/project/visionagent`로 이동한 후, 아래 명령어들을 실행하여 코드 실행이 가능합니다.
- `paranoma.py` 에서 사진읽기를 실행하기 위해서는 data에 이미지 파일이 존재해야 합니다.
```
python src/paranoma.py
python src/special_effect.py
```