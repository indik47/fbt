import sys
import unreal

def attach_to_debugger(host, port):
    try:
        # TODO : Use your PyCharm install directory.
        pydev_path = "C:\Program Files\JetBrains\PyCharm 2023.1.1\plugins\python\helpers\pydev"
        # pydev_path = r'C:\Users\denys.oligov\AppData\Local\Programs\Python\Python39\Lib\site-packages'

        if not pydev_path in sys.path:
            sys.path.append(pydev_path)
        import pydevd
        pydevd.stoptrace()
        pydevd.settrace(
            port=port,
            host=host,
            stdoutToServer=True,
            stderrToServer=True,
            overwrite_prev_trace=True,
            suspend=False,
            trace_only_current_thread=False,
            patch_multiprocessing=False,
        )
        print("PyCharm Remote Debug enabled on %s:%s." % (host,port))
    except:
        import traceback
        traceback.print_exc()
        
        print(f'---------------------------Couldnt connect on {port}')

attach_to_debugger('localhost', 60059)

# import fbyte.source.camera.tightrope_screenshot_creator as tsc
# from importlib import reload
# reload(tsc)
# 
# tsc.main2()
# 
# unreal.log("www")
# unreal.log("Done")