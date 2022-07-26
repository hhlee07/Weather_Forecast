import numpy as np
import json, os
import cv2
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from dateutil.relativedelta import relativedelta
from tqdm import tqdm, trange

def cal_dist(mlat, mlon, olat, olon):
    return np.sqrt((mlat - olat)**2 + (mlon - olon)**2)

def find_nearest(olat, olon, mlat, mlon):
    dist = cal_dist(mlat, mlon, olat, olon)
    nx, ny = np.unravel_index(dist.argmin(), dist.shape)
    return ny, nx


def make_line(pos_list, array):
    img_array = Image.fromarray(array)
    draw = ImageDraw.Draw(img_array)
    draw.line((pos_list), fill='white', width=100)
    re_array = np.array(img_array)
    re_array[np.where(re_array>100.0)]=1
    return(re_array)

def find_value(sdate, edate, in_dir, out_dir, grid_file):
    fmt = '%Y%m'
    dt_sdate = datetime.strptime(sdate, fmt)
    dt_edate = datetime.strptime(edate, fmt)
    now = dt_sdate
    grid = np.load(grid_file)
    mlat = grid[0,:,:]
    mlon = grid[1,:,:]
    
    #annotations
    #choose one
    #names = np.array(['LLJ', 'W_SNOW','E_SNOW','WET_SN','CUM_SN','COLD_FRONT','WARM_FRONT','OCC_FRONT','H_POINT','L_POINT'
    #        ,'HLJ', 'TYPOON', 'R_START', 'R_STOP','RA_SN','HAIL'])
    # class는 타이푼으로 설정
    name = 'TYPOON'

    os.makedirs(os.path.join(out_dir, name + '_img'), exist_ok=True)
    while now <= dt_edate:
        print(now)
        str_now = datetime.strftime(now, '%Y%m')
        file_list = os.listdir('%s/%s'%(in_dir, str_now))
        count = 0
        if len(file_list) == 0:
            continue
        else:
            for i in trange(len(file_list)):
                file_name = file_list[i]
                check = 0
                masks = np.zeros((3000,2600))
                with open('%s/%s/%s'%(in_dir, str_now, file_name), 'r') as json_file:
                    json_data = json.load(json_file)
                now_color = 255
                name_count = 0
                for datas in json_data['features']:
                    now_name =  datas['properties']['name']
                    if now_name == name:
                        name_count +=1
                if name_count == 0 :
                    continue
                
                
                for datas in json_data['features']:
                    now_name =  datas['properties']['name']
                    if name != now_name :
                        continue
                    now_type = datas['geometry']['type']
                    spot_list = datas['geometry']['coordinates']
                    pos_list = []
                    if now_type == 'Point' :
                        spot_list = [spot_list]
                    if now_type == 'Polygon' :
                        spot_list = spot_list[0]
                    try : 
                        for olon, olat in spot_list:
                            pos_list.append(find_nearest(olat, olon, mlat, mlon))
                    except Exception as e:
                        print(e)
                        print(str_now,file_name)
                    pos_list = np.array(pos_list)
                    check +=1
                    if now_type == 'LineString':
                        masks = cv2.polylines(masks,[pos_list],isClosed=False,color=now_color,thickness=50)
                    elif now_type == 'Point' : 
                        masks = cv2.circle(masks,pos_list[0],50,now_color,-1)
                    elif now_type == 'Polygon' :
                        masks = cv2.fillPoly(masks,[pos_list],now_color)

                if check>=1:
                    tempmask = masks
                    tempmask = np.rot90(tempmask)
                    tempmask = Image.fromarray(tempmask)
                    tempmask = tempmask.crop((1050,850,1950,1750))
                    tempmask = np.array(tempmask)
                    tempmask = tempmask.astype(np.uint8)
                    if tempmask.max() == 0:
                        continue
                    cv2.imwrite('%s/%s_img/%s.png'%(out_dir, name, file_name[:12]),tempmask)
                    #np.save('%s/%s/%s.png'%(out_dir, name,file_name[:12]), tempmask)
        now = now+relativedelta(months=1)

#startdate yyyymm
sdate = '201907'
#enddate yyyymm
edate = '202006'
#input geojson directory
in_dir = '/hd/기상분석데이터/기상분석_train/master'
#output mask directory
out_dir = '/hd/geojson'
#grid numpy file location
grid_file = '/weather/ea_2km_latlong.npy'
#make mask
find_value(sdate, edate, in_dir, out_dir, grid_file)