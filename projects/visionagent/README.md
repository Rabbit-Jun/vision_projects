## paranoma

-  컴퓨터와 연결된 캠을 이용하여 파라노마를 만들고 해당 파라노마를 꾸밀 수 있는 기능을 구현하였습니다.  
-  파일을 저장할 때 png, jpg 와 같은 확장자를 사용해야 합니다.
-  그리기 해제를 한 후 저장을 해야 사각형이 사라진채로 저장됩니다.


### *사용 방법*
1. 촬영 버튼을 누른 후 c를 이용하여 이미지를 겹치게 촬영합니다. (*완전히 동일한 장면일 경우 파라노마 기능을 사용할 수 없습니다*)
2. 파라노마를 클릭하여 파라노마를 만들어 줍니다.
3. 글자 마우스의 좌측(*사각형의 시작 좌표*)과 우측(*사각형의 끝 좌표*)를 이용하여 사각형을 생성해 줍니다.
4. 글자 입력을 통해 사각형 안에 글자를 입력합니다.
5. 그리기 버튼을 통해 파라노마에 그림을 그립니다.
6. 그리기 해제를 누르면 다시 사각형을 생성할 수 있습니다(*그리기 이후 그리기 해제를 하여야 삭가형이 사라진채로 저장됩니다*)
7. 되돌리기를 이용하여 이전 상황으로 되돌릴 수 있습니다.

## special_effect

## Folder Structure

```
visionagent
├── data
│ 
├── build
│ └──paranoma
│ └──special_effect
├── dist
│ └──paranoma.exe
│ └──special_effect.exe
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
- 
### paranoma
```
python src/paranoma.py 
dist/paranoma.exe
```
### special_effect
```
python src/special_effect.py
dist/special_effect.exe
```