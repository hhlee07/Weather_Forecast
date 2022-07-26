import os

# gt만 존재하고 input image는 존재하지 않는 데이터가 있어서 삭제
file_list = os.listdir('/hd/geojson/TYPOON_img')
for f in file_list:
    if not os.path.exists('/hd/hackathon/train/위성/천리안2호/ir112/' + f[:6] + '/' + f[:-4] + '_KOMPSAT2A_KO_IR112.png'):
        os.remove('/hd/geojson/TYPOON_img/' + f)