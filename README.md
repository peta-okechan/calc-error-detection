# 計算誤差の検出

以下の問題を解くプログラム。
http://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11136503501
リンク先ではなるべく実行が速く、なるべくコードが短いという点が
評価軸になっているが、極めて個人的な趣味によりその辺りは投げ捨て
読み易さを優先して本プログラムを作成した。

問題(1):
4個の一桁の数値に対する四則演算の結果が
'分数の計算をちゃんとやれば'本当は10になるのに
整数演算だと誤った結果になる例を全て出力。

問題(2):
問題(1)の浮動小数点数版。

## 使い方:
`$ python calc-error-detection.py int`
`$ python calc-error-detection.py float`

## 出力:
式 = 真の答え (誤差を含んだ答え)
式 = 真の答え (誤差を含んだ答え)
式 = 真の答え (誤差を含んだ答え)
...

## 注意点:
枝刈りとかしてないので激遅です。
NaNを表現するためにNoneを使用しています。

## 動作確認環境:
`$ cat /etc/redhat-release
Fedora release 22 (Twenty Two)
$ uname -rvo
4.0.4-303.fc22.x86_64 #1 SMP Thu May 28 12:37:06 UTC 2015 GNU/Linux
$ python -V
Python 2.7.10`
