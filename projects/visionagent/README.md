### 목적
-  `panorama`: 자신만의 스타일로 이미지를 꾸미고 싶은 사람을 위해 만들었습니다. 
-  `special_effect`: 특정 부분을 색다른 시선으로 바라보며 새로운 영감을 얻고 싶어하는 사람을 위해 만들었습니다. 

## panorama

-  컴퓨터와 연결된 캠을 이용하여 파라노마를 만들고 해당 panorama를 꾸밀 수 있는 기능을 구현하였습니다.  
-  파일을 저장할 때 png, jpg 와 같은 확장자를 사용해야 합니다.
-  그리기 해제를 한 후 저장을 해야 사각형이 사라진채로 저장됩니다.
-  사용자가 보기 편하게 `cv2.flip()`을 이용해 좌우 반전 시켰습니다


### *사용 방법*
1. 촬영 버튼을 누른 후 c를 이용하여 이미지를 겹치게 촬영합니다. (*완전히 동일한 장면일 경우 panorama 기능을 사용할 수 없습니다*)
2. panorama를 클릭하여 panorama를 만들어 줍니다.
3. 글자 마우스의 좌측(*사각형의 시작 좌표*)과 우측(*사각형의 끝 좌표*)를 이용하여 사각형을 생성해 줍니다.
4. 글자 입력을 통해 사각형 안에 글자를 입력합니다.
5. 그리기 버튼을 통해 파라노마에 그림을 그립니다.
6. 그리기 해제를 누르면 다시 사각형을 생성할 수 있습니다(*그리기 이후 그리기 해제를 하여야 삭가형이 사라진채로 저장됩니다*)
7. 되돌리기를 이용하여 이전 상황으로 되돌릴 수 있습니다.

## special_effect

- 컴퓨터와 연결된 캠을 이용하여 비디오를 시작했을 때 클릭을 통해 원하는 공간에 필터를 적용할 수 있게 만들었습니다.
- 파일을 저장할 때 png, jpg 와 같은 확장자를 사용해야 합니다.
- 사용자가 보기 편하게 `cv2.flip()`을 이용해 좌우 반전 시켰습니다

### *사용 방법*
1.  비디오 시작을 눌러 비디오를 켜줍니다.
2.  필터를 적용하길 원하는 공간을 클릭합니다
3.  비디오 시작 옆에 있는 버튼을 이용하여 원하는 필터를 적용합니다.
4. `c`로 캡쳐하고 `q`로 종료합니다. (*비디오 시작시 열리는 Special effect를 창을 클릭해야 key가 작용합니다*)

## Folder Structure

```
visionagent
├── data
│ 
├── build
│ └──panorama
│ └──special_effect
├── dist
│ └──panorama.exe
│ └──special_effect.exe
├── src
│ └── panorama.py 
│ └── special_effect.py
│
├── environment.yaml
└── poetry.lock
│
├── pyproject.toml
└── README.md
```

## Environment

- Anaconda Powerell Prompt

## conda에서 라이브러리 설치 방법
`environment.yaml`이 있는 visionagent 디렉터리에서 아래의 명령어를 실행합니다.
```powershell
conda env create -f environment.yaml
```
그 후 생성된 가상환경 `vision`을 활성화 시키고 `pip install PyQt6` 해줍니다.  

## poetry에서 라이브러리 설치 방법
`pyproject.toml`이 있는 visionagent 디렉터리에서 아래의 명령어를 실행합니다.
```powershell
poetry install
``` 


## 코드 실행

- `/visionagent`로 이동한 후, 아래 명령어들을 실행하여 코드 실행이 가능합니다.
 
### panorama
```powershell
python src/panorama.py  # 스크립트 파일 실행
dist/panorama.exe  # exe 파일 실행
```
### special_effect
```powershell
python src/special_effect.py  # 스크립트 파일 실행
dist/special_effect.exe  # exe 파일 실행
```