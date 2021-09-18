# 1. 이미지 파일과 라벨을 불러온다
# 2. 박스 좌표를 불러온다
import json

def get_img(path):
    return img

def get_bbox(path):
    with open(path, "r") as st_json:
        data = json.load(st_json)
        
        # 데이터 없는 사진은 제외
        if data["annotations"]==[]:
            pass

        else:
            for i in range(len(data["annotations"])):
                # 겟오프 부분만 가져와서
                get_off = data["annotations"][i]["get_off"]
                # 하차하는 사람이 있다면
                if get_off == True:
                    person_id = data["annotations"][i]["id"]
                    is_getoff_true+= 1

if __name__=="__main__":
