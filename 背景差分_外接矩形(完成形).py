import numpy as np
import cv2
import matplotlib.pyplot as plt


# 画像の読み込み
img_src1 = cv2.imread("/home/pi/gazou/haikei.jpg", 1)   #背景のみの画像
img_src2 = cv2.imread("/home/pi/gazou/coin.jpg", 1)   #物が写っている画像

img_src1 = img_src1[20:450, 150:580]    #物が写っている部分と同じ領域の切り出し
img_src2 = img_src2[20:450, 150:580]    #対象物とその周辺のみを切り出し

"""
#グレースケール変換（必要なら）
img_src1 = cv2.cvtColor(img_src1, cv2.COLOR_BGR2GRAY)
img_src2 = cv2.cvtColor(img_src2, cv2.COLOR_BGR2GRAY)
"""
#背景差分をするためのアルゴリズム3種（状況に応じて変えることがあるかも？）
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg = cv2.createBack変換groundSubtractorMOG2() 
#fgbg = cv2.bgsegm.createBackgroundSubtractorGSOC()

#画像をアルゴリズムに入れる
fgmask = fgbg.apply(img_src1)
fgmask = fgbg.apply(img_src2)

# 表示
cv2.imshow('frame',fgmask)
cv2.waitKey(0)

# 検出画像 (二値画像で表示される）
bg_diff_path  = 'home/pi/gazou/sabun.jpg'
cv2.imwrite('/home/pi/gazou/sabun.jpg',fgmask)
cv2.waitKey(1)

"""
# 色の反転（必要なら）
coins_binary = cv2.bitwise_not(coins_binary)
cv2.imshow("white", coins_binary)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/coins_binary.jpg', coins_binary)
"""

# 輪郭検出（黒と白の境界線を輪郭とする）
_, coins_contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# coins_and_contoursに元の画像をコピー
coins_and_contours = np.copy(img_src2)


#ここから他の場合と同じ------------------------------------------------------------------------------------------------

# 何個かあるかカウント
min_coin_area = 60
large_contours = [cnt for cnt in coins_contours if cv2.contourArea(cnt) > min_coin_area]
 
# 輪郭を描写　（引数　＝＝＝　1：入力画像	2：listとして保存されている輪郭	3：listの何番目の輪郭か（−1なら全部）	4~：輪郭線の情報）
coin=cv2.drawContours(coins_and_contours, large_contours, -1, (255,0,0))
 
# カウントした個数の表示
print('number of coins: %d' % len(large_contours))

cv2.imshow("white", coin)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/coinsdraw.jpg', coin)

# coinsをコピー
bounding_img = np.copy(img_src2)
 
# 外接矩形の描写
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
   
cv2.imshow("white", gaisetu)
cv2.waitKey(0)


#外接矩形で切り取る
for contour in large_contours:
    x, y, w, h = cv2.boundingRect(contour)
    gaisetu = cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    crop = gaisetu[y:y+h, x:x+w]
    cv2.imshow("white", crop)
    cv2.waitKey(0)



#ここから合成(別途上げるが、試したついでにそのまま）------------------------------------------------------------


gousei = cv2.imread('/home/pi/gazou/gousei.jpg')
gousei2 = crop

white_size = gousei.shape[:2]
hantei_size = gousei2.shape[:2]
print(white_size)

if hantei_size[0] > white_size[1] or hantei_size[1] > white_size[0]:
        raise Exception("img is larger than size")

row = (white_size[1] - hantei_size[0]) // 2
col = (white_size[0] - hantei_size[1]) // 2
gousei[row:(row + hantei_size[0]), col:(col + hantei_size[1])] = gousei2
print(gousei.shape[:2])
cv2.imshow("white2", gousei)
cv2.imwrite('/home/pi/gazou/white_gousei.jpg', gousei)
cv2.waitKey(0)
