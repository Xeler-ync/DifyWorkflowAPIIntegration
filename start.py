import platform
from multiprocessing import Process, Pipe, set_start_method

import main
import training.scripts.api as api

if __name__ == "__main__":

    # # 根据操作系统设置不同的启动方式
    # if platform.system() == "Windows":
    #     set_start_method("spawn", force=True)
    # else:
    #     set_start_method("fork", force=True)

    (tornadoPipe, trainingPipe) = Pipe()

    TornadoProcess: Process = Process(target=main.main, args=(tornadoPipe,))
    TrainingProcess: Process = Process(target=api.start, args=(trainingPipe,))

    TornadoProcess.start()
    TrainingProcess.start()

    TornadoProcess.join()
    TrainingProcess.join()
