import numpy as np
import cv2
import matplotlib.pyplot as plt

#読み込む画像の指定
print('画像の名前を入力してください。 \n画像は/home/pi/gazou/フォルダ内の物に限ります')
file_name = input()	#画像名の取得
path = '/home/pi/gazou/'+file_name+'.jpg'

origin = cv2.imread(path)	#画像の読み込み
origin = origin[20:450, 150:580]
gray = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)	#画像をグレースケールに変換
preprocessed = cv2.GaussianBlur(gray, (5, 5), 0)	#画像のぼかし

cv2.imshow("gray&gaus", preprocessed)	#画像の表示
cv2.waitKey(1)
cv2.imwrite('/home/pi/gazou/'+file_name+'_preprocessed.jpg', preprocessed)	#画像の保存
cv2.waitKey(1)
# 画像の閾値処理
_, origin_binary = cv2.threshold(preprocessed, 130, 255, cv2.THRESH_BINARY)

# 色の反転
#coins_binary = cv2.bitwise_not(coins_binary)
cv2.imshow("binary", origin_binary)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/'+file_name+'_binary.jpg', origin_binary)

# 輪郭検出
_, origin_contours, _ = cv2.findContours(origin_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# 元の画像をコピー
origin_and_contours = np.copy(origin)

# 何個かあるかカウント
min_coin_area = 60
large_contours = [cnt for cnt in origin_contours if cv2.contourArea(cnt) > min_coin_area]
 
# 輪郭を描写　（引数　＝＝＝　1：入力画像	2：listとして保存されている輪郭	3：listの何番目の輪郭か（−1なら全部）	4~：輪郭線の情報）
origin_contour = cv2.drawContours(origin_and_contours, large_contours, -1, (255,0,0))
 
# カウントした個数の表示
print('number of coins: %d' % len(large_contours))

cv2.imshow("origin_contours", origin_contour)
cv2.waitKey(1)
cv2.imwrite('/home/pi/gazou/'+file_name+'_draw.jpg', origin_contour)

# 元の画像をコピー
bounding_img = np.copy(origin)
 
# 外接矩形の描写
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 0, 0), 1)
cv2.imshow("gaisetu", gaisetu)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/'+file_name+'_gaisetu.jpg', gaisetu)


i = 1
#外接矩形で切り取る
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    crop = gaisetu[y:y+h, x:x+w]
    cv2.imshow("white3", crop)
    cv2.waitKey(0)
    cv2.imwrite('/home/pi/gazou/'+file_name+'kiritori'+str(i)+'.jpg', crop)
    cv2.waitKey(1)
    i = i + 1
