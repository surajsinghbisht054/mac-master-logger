import sys
from pyparsing import Word, alphas, Suppress, Combine, nums, string, Optional, Regex
from time import strftime

class Parser(object):
  def __init__(self):
    ints = Word(nums)
    textt = Word(alphas)
    # LOG LEVEL
    log_level = Suppress("[") + textt + Suppress("]")

    # timestamp
    month = Combine(ints + "-" + ints + "-" + ints)
    hour  = Combine(ints + ":" + ints + ":" + ints)    
    timestamp = month + hour

    # # hostname
    # hostname = Word(alphas + nums + "_" + "-" + ".")

    # # appname
    # appname = Word(alphas + "/" + "-" + "_" + ".") + Optional(Suppress("[") + ints + Suppress("]")) + Suppress(":")

    # # message
    # message = Regex(".*")
  
    # pattern build
    # + timestamp + hostname + appname + message
    self.__pattern = log_level  + timestamp
    
  def parse(self, line):
    parsed = self.__pattern.parseString(line)

    payload              = {}
    payload["log_level"]  = parsed[0]
    payload["timestamp"] = strftime("%Y-%m-%d %H:%M:%S")
    # payload["hostname"]  = parsed[4]
    # payload["appname"]   = parsed[5]
    # payload["pid"]       = parsed[6]
    # payload["message"]   = parsed[7]
    
    return payload

""" --------------------------------- """

def main():
  parser = Parser()
  
  
  with open("simple.log") as syslogFile:
    for line in syslogFile:
      fields = parser.parse(line)
      print(fields)
      
main()