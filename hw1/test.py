import subprocess
import time

def test():
    sample_io_path = "./sample_io/"
    extra_testcases_path = "./extra_testcases/"
    for i in range(1, 5):
        print("Test ", i, " ...")
        start = time.time()
        subprocess.run(f"python3 e2448835_hw1.py < {sample_io_path}in{i} > {sample_io_path}myout{i} ", shell=True)
        end = time.time()
        # wait for the subprocess to finish

        with open(f"{sample_io_path}out{i}", "r") as f1:
            with open(f"{sample_io_path}myout{i}", "r") as f2:
                output = f2.read()
                expected = f1.read()
                if expected == output:
                    print(f"Test {i} Passed")
                else:
                    print(f"Test {i} Failed")
                    print("Expected:\n", expected)
                    print("Output:\n", output)
                    print("Difference:\n", set(expected.split()) - set(output.split()))
        print("Execution time: ", "{:.2f}".format(end-start) , " seconds")
        print("****************************************************************************************\n\n")

    for i in range(1,5)[::-1]:
        print("Extra Test ", i, " ...")
        start = time.time()
        subprocess.run(f"python3 e2448835_hw1.py < {extra_testcases_path}in{i} > {extra_testcases_path}myout{i}", shell=True)
        end = time.time()
        # wait for the subprocess to finish

        with open(f"{extra_testcases_path}out{i}", "r") as f1:
            with open(f"{extra_testcases_path}myout{i}", "r") as f2:
                if f1.read() == f2.read():
                    print(f"Test {i} Passed")
                else:
                    print(f"Test {i} Failed")
        print("Execution time: ", "{:.2f}".format(end-start) , " seconds")
        print("****************************************************************************************")

    


test()
    
