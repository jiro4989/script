# coding: utf-8

from datetime import datetime
from time import sleep
from sys import stdout
import time
import sys
import re
import pyaudio
import wave

u"""
引数のチェック
引数の一つ目は音を鳴らすタイミングと音声ファイルを記述したテキストファイル
"""
if len(sys.argv) < 2:
	print(u'コマンドライン引数が不足しています。')
	print(u'args[1] = time.csv')
	for (i,a) in enumerate(sys.argv):
		print(str(i) + ' - ' + a)
	exit()

CHUNK = 1024

u"""
渡されたwavファイルを鳴らす
@param filename wavfile
"""
def play_music(filename):
	filename = './audio/lu.wav'
	wf = wave.open(filename, 'rb')

	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			rate=wf.getframerate(),
			output=True)

	# 1024個読み取り
	data = wf.readframes(CHUNK)

	while len(data) != 0:
		stream.write(data)          # ストリームへの書き込み(バイナリ)
		data = wf.readframes(CHUNK) # ファイルから1024個*2個の

	stream.stop_stream()
	stream.close()

	p.terminate()

u"""
タイムミリ秒を返す関数
@param h 時間
@param m 分
"""
def mktime(h, m):
	date = datetime.today()
	t = datetime(date.year, date.month, date.day, h, m, 0)
	t = t.timetuple()
	t = time.mktime(t)
	return t

u"""
文字列配列を数値型タプルに変換して返却
"""
def int2(hm):
	return (int(hm[0]), int(hm[1]))

# 色文字列生成関数を返す
def getcolor(colorname):
	colors = {
			'clear'  : '\033[0m' ,
			'black'  : '\033[40m',
			'red'    : '\033[41m',
			'green'  : '\033[42m',
			'yellow' : '\033[43m',
			'blue'   : '\033[44m',
			'purple' : '\033[45m',
			'cyan'   : '\033[46m',
			'white'  : '\033[47m'
			}
	def f(c):
		return colors[colorname] + c + colors['clear']
	return f

# 色文字列生成関数
red    = getcolor('red')
yellow = getcolor('yellow')
green  = getcolor('green')

# 各種時間に対応した時間文字列を生成する
def mk_time_text(hour, minute, second):
	text = '%02d:%02d:%02d\r' % (hour, minute, second)
	if hour <= 0 and minute <= 3:
		return red(text)
	elif hour <= 0 and minute <= 5:
		return yellow(text)
	else:
		return green(text)

# 時間定数
MINUTE = 60
HOUR   = 60 * MINUTE

# csvファイルからタイマーのタイミングを読み込み
timelines = open(sys.argv[1], 'r').readlines()
timelines = [l for l in timelines if not l.startswith('#')]
timelines = [l for l in timelines if not re.match('^$', l)]
csv = [l.split(',') for l in timelines]

# 時刻を取得
timeline = csv[0][0]
tl = timeline.split(':')
(h, m) = int2(tl)
nexttime = mktime(h,m)

# 時刻リストの末尾に到達するまでループ
count = 0
while True:
	nowtime = datetime.today()
	nowtime = nowtime.timetuple()
	nowtime = time.mktime(nowtime)

	diff   = nexttime - nowtime
	hour   = int(  diff / HOUR)
	minute = int(( diff % HOUR) / MINUTE)
	second = int(((diff % HOUR) % MINUTE))

	# 色を変更して残り時間を標準出力
	text = mk_time_text(hour, minute, second)
	stdout.write(text)

	if (hour <= 0 and minute <= 0 and second <= 0) or (hour < 0):
		count += 1

		if len(timelines) <= count:
			break

		current = csv[count]
		(h, m) = int2(current[0].split(':'))
		nexttime = mktime(h,m)
		play_music(csv[count][1])

	sleep(1)

print(u"""
本日の業務は終了です。
お疲れ様でした。
また明日も頑張りましょう！
""")
