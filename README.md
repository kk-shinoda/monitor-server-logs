# monitor-server-logs

## プログラムの実行方法

本リポジトリの構成は以下のとおり。

![constitution](https://user-images.githubusercontent.com/86135975/127794940-fcfba8f2-4526-4fbd-9c48-23ff1538ac48.png)

実行方法は

カレントディレクトリを上図のrootにした状態で以下のコマンドを叩くことで実行することができる。

```bash
python Answers/answer_1.py
```

監視するログファイルはLogDataの中にまとめてある。

ログファイルは各answer.pyのmain関数にて読み込みが行われている。ファイルの指定はここに直接書き込む仕様である。
