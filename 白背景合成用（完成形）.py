#別途用意した白のみの画像に切り出した外接矩形を貼りつける
#tensorflow、keras といった機械学習では画像サイズを統一する必要がある
#切り出した画像をkerasでresizeしてもいいが、大きいものの場合こちらで揃えても良いかもしれない
#関数にしてないので、実践用は関数名をつけて、関数として使う

#2種の画像の準備
gousei = cv2.imread('/home/pi/gazou/gousei.jpg')        #白のみの画像を読み込み(サイズの調整をした画像が良い）
gousei2 = crop                                          #外接矩形で切り出した画像を指定(cropは保存してあるプログラムのままなら、切り出した画像)

white_size = gousei.shape[:2]           #白画像のサイズを取得
hantei_size = gousei2.shape[:2]         #切り出し画像のサイズを取得

if img_size[0] > size[1] or img_size[1] > size[0]:      #背景用の白画像より切り出し画像が大きい場合は警告だす
        raise Exception("背景が小さいです")

row = (white_size[1] - hantei_size[0]) // 2             #切り出し画像を中心におくための座標計算
col = (white_size[0] - hantei_size[1]) // 2
gousei[row:(row + hantei.shape[0]), col:(col + hantei.shape[1])] = gousei2      #白画像の指定座標に画像を貼り付け
cv2.imshow("white2", filled)
cv2.waitKey(0)
