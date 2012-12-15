import re
import sys
import itertools as it
import glob,os

class markovChatBot(object):
    def __init__(self):
        self.requestDict = {}
        self.replyDict = {}
        
    def add_all_chats(self, directory):
        for filename in glob.glob(os.path.join(directory, '*.txt')):
            self.addChatToBot(filename)
        print self.replyDict
        print self.requestDict

    def addChatToBot(self, filename):
        with open(filename, 'r') as chatlog:
            end_key = ''
            for line in chatlog:
                match =  re.match("^[0-9]+:[0-9]+ .* (.*): (.*)", line)
                if match:
                    if match.group(1) == 'me':
                        self.add_line_self(match.group(2))
                    self.dict_append(self.requestDict, end_key, match.group(2).split()[0])
                    end_key = ((match.group(1), ' '.join(match.group(2).split()[-2:])))

    def dict_append(self, dict_to_append, key, value):
        if key in dict_to_append:
            dict_to_append[key].append(value)
        else:
            dict_to_append[key] = [value]

    def add_line_self(self, chatline):
        #print chatline
        first, second, value = it.tee(chatline.split(), 3)
        second.next()
        value.next()
        try:
            value.next()
        except(StopIteration):
            pass
        splitline = it.izip_longest(first, second, value)
        for first, second, value in splitline:
            #print (first,second,value)
            if second is None:
                key = first
            else: 
                key = " ".join((first, second))

            if key in self.replyDict:
                self.replyDict[key].append(value)
            else:
                self.replyDict[key] = [value]
            
if __name__ == '__main__':
    m = markovChatBot()
    print sys.argv[1]
    m.add_all_chats(sys.argv[1])
