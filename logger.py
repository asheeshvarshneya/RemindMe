def WriteLogEvent(LogFile, EventString):
    import time
    import datetime
    LogFileHandle=open(LogFile,"a");
    mytime = time.ctime(time.time())
    str="<<"+mytime+">>:"+EventString+"\n"
    LogFileHandle.write(str);
    LogFileHandle.close();

def WriteEvent(LogFile, EventString):
    LogFileHandle=open(LogFile,"a");
    str="\n" + EventString
    LogFileHandle.write(str);
    LogFileHandle.close();

