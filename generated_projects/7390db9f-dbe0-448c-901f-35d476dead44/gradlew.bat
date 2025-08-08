@echo off
if not defined PROG do set PROG=%0
call "%PROG%" --sys-prop org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8 "%@"
