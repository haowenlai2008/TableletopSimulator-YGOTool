
import os
import os.path
import PIL.Image as Image
import re
import sys
deckPath = './deck/'    # 输出的卡组目录
picsPath = './Pics/'    # 卡图库目录
def dealYDK(ydkPath):
    ydk = ''
    with open(ydkPath, encoding='utf8') as f:
        ydk = str(f.read());
    pattern1 = re.compile(r'#main(.|\n)*?#extra')
    pattern2 = re.compile(r'#extra(.|\n)*?!side')
    pattern3 = re.compile(r'!side(.|\n)*')
    mainDeck = []   # 主卡组密码列表
    exDeck = []     # 额外卡组密码列表
    sideDeck = []   # 副卡组密码列表
    for e in re.finditer(pattern1, ydk):
        mainDeck = e.group()[6:-7].split('\n')
        while '' in mainDeck:
            mainDeck.remove('')
    for e in re.finditer(pattern2, ydk):
        exDeck = e.group()[7:-6].split('\n')
        while '' in exDeck:
            exDeck.remove('')
        
    for e in re.finditer(pattern3, ydk):
        sideDeck = e.group()[6:].split('\n')
        while '' in sideDeck:
            sideDeck.remove('')
    return mainDeck, exDeck, sideDeck

#根据卡片代码列表生成图片，deckName是卡组名称，filename是文件名
def generateOutImage(codeList, deckName, fileName):
    weith = 322 # 图片宽度
    height = 470    # 图片高度
    index = 0
    toImage = Image.new('RGB', (weith * 10, height * 7))    # 图片大小
    timeToBreak = False;
    # 拼图
    for y in range(7):
        if timeToBreak:
            break
        for x in range(10):
            fromImage = Image.open(picsPath + codeList[index] + '.jpg')
            toImage.paste(fromImage, (x * weith, y* height))
            index += 1
            if index >= len(codeList):
                timeToBreak = True;
            if timeToBreak:
                break
    # 判断路径是否存在，不存在就创建
    path = deckPath + deckName
    if not os.path.exists(path):
        os.makedirs(path)
    filePath = path + '/' + fileName + '.jpg'
    toImage.save(filePath)  # 导出图片
    print('save:' + filePath)
    
ydkPath = sys.argv[1]   # 从命令行获得卡组文件路径
ydkObj = ydkPath.split('\\')    
while '' in ydkObj:
    ydkObj.remove('')
ydkName = ydkObj[-1]
deckName = ydkName[:-4] # 获得卡组文件名
print(ydkName)
mainDeck, exDeck, sideDeck = dealYDK(ydkPath)
generateOutImage(mainDeck, deckName, deckName + '_main')
generateOutImage(exDeck, deckName, deckName + '_ex')
generateOutImage(sideDeck, deckName, deckName + '_side')








