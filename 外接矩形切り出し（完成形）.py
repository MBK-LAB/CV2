import numpy as np
import cv2
import matplotlib.pyplot as plt

#読み込む画像の指定
path = '/home/pi/gazou/coin.jpg'

coins = cv2.imread(path)	#画像の読み込み
coins = coins[20:450, 150:580]
coins_gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)	#画像をグレースケールに変換
coins_preprocessed = cv2.GaussianBlur(coins_gray, (5, 5), 0)	#画像のぼかし

cv2.imshow("coin", coins_preprocessed)	#画像の表示
cv2.waitKey(1)
cv2.imwrite('/home/pi/gazou/2coins_preprocessed.jpg', coins_preprocessed)	#画像の保存
cv2.waitKey(1)
# 画像の閾値処理
_, coins_binary = cv2.threshold(coins_preprocessed, 90, 255, cv2.THRESH_BINARY)

# 色の反転
#coins_binary = cv2.bitwise_not(coins_binary)
cv2.imshow("coin_bw", coins_binary)
cv2.waitKey(1)
cv2.imwrite('/home/pi/gazou/2coins_binary.jpg', coins_binary)

# 輪郭検出
_, coins_contours, _ = cv2.findContours(coins_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# coins_and_contoursにcoinsをコピー
coins_and_contours = np.copy(coins)
 
# 何個かあるかカウント
min_coin_area = 60
large_contours = [cnt for cnt in coins_contours if cv2.contourArea(cnt) > min_coin_area]
 
# 輪郭を描写　（引数　＝＝＝　1：入力画像	2：listとして保存されている輪郭	3：listの何番目の輪郭か（−1なら全部）	4~：輪郭線の情報）
coin=cv2.drawContours(coins_and_contours, large_contours, -1, (255,0,0))
 
# カウントした個数の表示
print('number of coins: %d' % len(large_contours))

cv2.imshow("coin_contours", coin)
cv2.waitKey(1)
cv2.imwrite('/home/pi/gazou/2coinsdraw.jpg', coin)

# coinsをコピー
bounding_img = np.copy(coins)
 
# 外接矩形の描写
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
cv2.imshow("coin_gaisetu", gaisetu)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/gaisetu.jpg', gaisetu)


i = 1
#外接矩形で切り取る
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    crop = gaisetu[y:y+h, x:x+w]
    cv2.imshow("white3", crop)
    cv2.waitKey(0)
    cv2.imwrite('/home/pi/gazou/2kiritori'+str(i)+'.jpg', crop)
    cv2.waitKey(1)
    i = i + 1
