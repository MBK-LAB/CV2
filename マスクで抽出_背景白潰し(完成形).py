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
cv2.imwrite('/home/pi/gazou/coins_maski.jpg', coins_binary)


#ここまで外接矩形切り出しと一緒--------------------------------------------------------------------------------------------------


#マスク処理
img_masked = cv2.bitwise_and(coins, coins, mask=coins_binary)   #coinsをcoins_binaryでマスク処理
cv2.imshow("coins", img_masked)
cv2.waitKey(0)
cv2.imwrite('/home/pi/gazou/coins_,masked.jpg', img_masked)
cv2.waitKey(1)

black = [0,0,0]   #blackに黒色の情報
white = [255, 255, 255]  #whiteに白色の情報
img_masked[np.where((img_masked == black).all(axis=2))] = white   #img_maskedのblack(黒色)と一致するピクセルwをwhite(白色)に変換
cv2.imshow('white', img_masked)
cv2.waitKey(0)



