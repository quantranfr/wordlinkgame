# -*- coding: utf8 -*-
import random
import re
import sys
import codecs
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def simplifyword(s):
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    s = re.sub(u'Ç', 'C', s)
    s = re.sub(u'ç', 'c', s)
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[ëèéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[îïìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÎÏÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ûüùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ÛÜƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u' ', '', s)
    return s

dic = []
dicmodif = []

def loaddic(l):
	global dic, dicmodif
	filename = {
		'v': "viet39k.txt",
		'e': "dic_en.txt"
	}
	dicfilename = filename[l]
	dicfile = open(dicfilename, "r")
	dic = []
	dicmodif = []
	for word in list(dicfile):
	    word = word.strip()
	    dic.append(word)
	    dicmodif.append(simplifyword(word))

def dicsurvey(wl):
	return [w for w in dicmodif if len(w)==wl]

def issublist(small, big):
	ls = small[:]
	lb = big[:]
	for letter in ls:
		if letter in lb:
			lb.remove(letter)
		else:
			return False
	return True

def solve(letterlist, wordlength):
	global dic, dicmodif
	res = []
	for i, w in enumerate(dicmodif):
		if len(w) == wordlength:
			if issublist(list(w), letterlist):
				res.append(dic[i])
	return res

def chooselang():
	lang = input("choose between Vietnamese/French/English (v/f/e): ")
	if lang not in ['v','e']:
		print("not supported yet")
		sys.exit()
	loaddic(lang)

def solveinterface():
	while True:
		letterlist = input("enter letters (no space no comma...): ")
		if letterlist=='': break
		letterlist = list(letterlist)

		while True:
			wordlength = input("enter word length: ")
			if wordlength == "": break
			wordlength = int(wordlength)
			res = solve(letterlist, wordlength)
			for r in res: print(r)

def playinterface():
	while True:
		level = input('choose level easy/medium/hard (e/m/h): ')
		if level not in ['e','m','h']: break
		quiz = makequiz(level)
		print('given these letters: ')
		print(''.join(quiz['letterlist']))
		for wl in quiz['ans']:
			wlist = quiz['ans'][wl]
			expectednb = min(5, len(wlist))
			print("write " + str(expectednb) + " words of " + str(wl) + " letters:")
			correctnb = 0
			while correctnb < expectednb:
				ans = input()
				if ans == '': break
				if ans in wlist:
					print("bingo.")
					wlist.remove(ans)
					correctnb = correctnb + 1
					if len(wlist) and correctnb<expectednb : print("another one?")
				else:
					print('try again. ')
		playagain = input("play again? (y/n): ")
		if playagain == 'n': break

def makequiz(level):
	quiz = {}
	sl = {
		'e': [3, 5],
		'm': [6, 9],
		'h': [10, 15]
	}
	seedlength = random.randint(sl[level][0], sl[level][1])
	quiz['seedlength'] = seedlength
	wllist = dicsurvey(seedlength)
	seed = wllist[random.randint(0, len(wllist)-1)]
	quiz['seed'] = seed
	quiz['letterlist'] = list(seed)
	random.shuffle(quiz['letterlist'])
	quiz['ans'] = {}
	for wl in range(max(2, seedlength-2), seedlength+1):
		res = solve(list(seed), wl)
		if len(res):
			quiz['ans'][wl] = res[:]
	return quiz

def main():
	chooselang()
	while True:
		mode = input("choose between PLAY mode and SOLVE mode (p/s): ")
		if mode == "": break
		if mode not in ['p','s']:
			print("wrong choice")
			continue
		if mode == 'p':
			playinterface()
		elif mode == 's':
			solveinterface()

if __name__ == '__main__':
	main()
