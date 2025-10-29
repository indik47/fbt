import sys
import unreal

def settrace():
    # sys.path.append(r'C:\Users\denys.oligov\AppData\Local\Programs\Python\Python39\Lib\site-packages') # ptvsd should be installed / located here
    sys.path.append(r'C:\temp\venv\Lib\site-packages') # ptvsd should be installed / located here
    
    import ptvsd
    ptvsd.enable_attach(address=('0.0.0.0', 3001), redirect_output=True)
 
    # pause the program until a remote debugger is attached
    ptvsd.wait_for_attach()
    ptvsd.break_into_debugger()

def main():
    print('lalalal333333')

    for p in sys.path:
        if 'pycharm' in p.lower():
            del sys.path[sys.path.index(p)]

    for p in sys.path:
        if 'pycharm' in p.lower():
            print(p)

    settrace()
    import fbyte.source.camera.tightrope_screenshot_creator as tsc

    tsc.main2()

main()

# unreal.log("www")
# unreal.log("Done")