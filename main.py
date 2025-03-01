from tester import CPUTaskTester

if __name__ == "__main__":
    tester = CPUTaskTester()
    tester.run_test(0)
    tester.compare_and_reset_results()
    tester.run_test(1)
    tester.compare_and_reset_results()
    tester.run_test(2)
    tester.compare_and_reset_results()
    tester.run_test(3)
    tester.compare_and_reset_results()
    tester.run_test(4)
    tester.compare_and_reset_results()
    tester.run_test(5)
    tester.compare_and_reset_results()
    tester.summarize_results()