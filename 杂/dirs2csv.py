from os import listdir, remove, getcwd
from pandas import read_csv, DataFrame
from time import sleep

path = input(r'复制文件夹的地址')
name = input('文件取名')
dir_list = listdir(path)
with open('{}.csv'.format(name), 'w', encoding='ANSI') as fs:
    fs.write('提,示:,修,改,此,行,内,容,占,位,la,la'+'\n')
for dir_name in dir_list:
    with open('{}.csv'.format(name), 'a', encoding='ANSI') as f:
        content = dir_name
        f.write(content.replace(' ', ',')+'\n')
# print('保存成功！！！记得在excel里面另存为xlsx文件')
sleep(2)
csv = read_csv('{}.csv'.format(name), encoding='ANSI')
csv.to_excel('{}.xlsx'.format(name), sheet_name='{}'.format(
    name), header=True, index=False)
sleep(2)
remove('{}\\{}.csv'.format(getcwd(), name))
print('保存路径在{}\n'.format(getcwd()))
input('按ENTER键结束')
