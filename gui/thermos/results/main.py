from os import path


base_dir = r'N:\multi_mg\LDN\ARP\execution'
base_input_path = path.join(base_dir, 'input_data')
base_output_path = path.join(base_dir, 'output_results')

allocation_input_path = path.join(base_dir, r'input_data\allocation_data')
strategy_input_path = path.join(base_dir, r'input_data\strategy_data')
allocation_output = path.join(base_dir, r'output_results\allocations')
strategy_output = path.join(base_dir, r'output_results\strategies')
thinkfolio_execution = path.join(base_dir, r'output_results\thinkfolio')


class DataLoader:

    def __init__(self):
        self.strategy_path = 'None'
        self.allocation_path = 'allocation_path'
        # self.signal_compiler = SignalCompiler(self.strategy_path)
        # self.allocation_compiler = AllocationCompiler(self.allocation_path)

    def read(self, file_path):
        pass

    def is_folder(self, file_path):
        return True

    def get_sub_names(self, file_path):
        pass

    def get_strategy_data(self, strategy_path, strategy_list):
        pass

    def get_allocation_data(self):
        pass
        # self.allocation_compiler.get_all_allocations()
