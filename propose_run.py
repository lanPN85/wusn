from wusn.propose.GA import *
import glob
import gc
import json
import threading
from multiprocessing import Process

run_times = 20


def run_propose(folder, out_folder):
    average_dict = {}
    current_path = os.path.abspath(os.path.dirname(__file__))
    my_path = os.path.join(current_path, folder, "*.test")
    out_path = os.path.join(current_path, "out", out_folder)
    files = glob.glob(my_path)
    count_instance = 0
    for file in files:
        list_times = []
        list_loss = []
        count_instance += 1
        count = 0
        #save_dir = os.path.join(current_path, "propose_out3", "file_" + str(count_instance))
        save_dir = os.path.join(out_path, "file_"+str(count_instance))
        os.makedirs(save_dir, exist_ok=True)
        for i in range(run_times):
            count += 1
            start_time = time.time()
            output = ga(file)
            run_time = time.time() - start_time
            list_times.append(run_time)
            list_loss.append(output.max_loss)
            print(file + "running time : " + str(count))
            output.to_text_file(file, os.path.join(save_dir, "result"+str(count)+".out"))
            output.plot_to_file(os.path.join(save_dir, "image"+str(count)+".png"))
            print("Running time for %d test: %.4f" % (count, run_time))
            gc.collect()
        avg_time = sum(list_times)/len(list_times)
        avg_loss = sum(list_loss)/len(list_loss)
        min_loss = min(list_loss)
        max_loss = max(list_loss)
        result_file = os.path.join(save_dir, "result_file.txt")
        # write to a dictionary
        if str(count_instance) not in average_dict:
            average_dict[count_instance] = [] # time, loss, min, max
        average_dict[count_instance].append(avg_time)
        average_dict[count_instance].append(avg_loss)
        average_dict[count_instance].append(min_loss)
        average_dict[count_instance].append(max_loss)
        # end complete dictionary
        with open(result_file, "wt") as f:
            f.write(str(file) + "\n")
            f.write("average time : " + str(avg_time) + "\n")
            f.write("average loss : " + str(avg_loss) + "\n")
            f.write("min loss     : " + str(min_loss) + "\n")
            f.write("max loss     : " + str(max_loss) + "\n")
            f.close()
        gc.collect()
    common_path = os.path.join(out_path, "common.txt")
    with open(common_path, "wt") as f:
        f.write(json.dumps(average_dict))
        f.close()
    gc.collect()


class RunThread(threading.Thread):
    def __init__(self, folder_in, folder_out):
        threading.Thread.__init__(self)
        self.folder_in = folder_in
        self.folder_out = folder_out

    def run(self):
        run_propose(self.folder_in, self.folder_out)


def run_medium():
    # run("medium_data", "MXF/medium/random")
    run_propose("medium_data/normal", "MXF/medium/normal")
    run_propose("medium_data/poisson", "MXF/medium/poisson")

#
# def run_normal_medium():
#     run_propose("medium_data/normal", "MXF/medium/normal")
#
#
# def run_poisson_medium():
#     run_propose("medium_data/poisson", "MXF/medium/poisson")


def run_large():
    run_propose('data', 'MXF/large/random')


if __name__ == '__main__':
    run_normal_medium = Process(target=run_propose, args=("medium_data/normal", "MXF/medium/normal"))
    #run_poisson_medium = Process(target=run_propose, args=("medium_data/poisson", "MXF/medium/poisson"))
    run_normal_medium.start()
    #run_poisson_medium.start()
    # run_normal_medium = RunThread("medium_data/normal", "MXF/medium/normal")
    # run_poisson_medium = RunThread("medium_data/poisson", "MXF/medium/normal")
    # run_normal_medium.start()
    # run_poisson_medium.start()
    # run("small_data", "small_data_MF")
    # run_medium()
    # run_large()