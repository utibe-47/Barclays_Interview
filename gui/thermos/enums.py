from enum import Enum, unique

from gui.thermos.helper_functions import scheduled_task_list, checks_to_run, jobs_list, pricing_source

task_list = scheduled_task_list()[1:]
ScheduledTaskEnum = Enum('ScheduledTaskEnum', {'_'.join(key.split()): value
                                               for key, value in zip(task_list, range(len(task_list)))})

job_list = jobs_list()
JobsEnum = Enum('JobsEnum', {'_'.join(key.split()): value
                             for key, value in zip(job_list, range(len(job_list)))})


checks = checks_to_run()
check_list = [chk[0] for chk in checks]
ConstraintsEnum = Enum('ConstraintsEnum', {'_'.join(key.split()): value
                                           for key, value in zip(check_list, range(len(check_list)))})


sources = pricing_source()
PriceSourcesEnum = Enum('PriceSourcesEnum', {key.lower(): value for key, value in zip(sources, range(len(sources)))})


class ProcessListEnum(Enum):
    run_prerun_checks = 0
    run_eda = 1
    run_strategy = 2
    run_constraints = 3
    run_thinkfolio_execution = 4
    send_signal_for_review = 5
    send_to_prod = 6
    send_recon_signal = 7


class ReasonCodes(Enum):
    rebalanc = 0
    posroll = 1


class AccessLevels(Enum):
    primary = 0
    secondary = 1


class StrategyGroup(Enum):
    value = 0
    momentum = 1
    carry = 2


@unique
class AccountNames(Enum):
    sbdi = 0
    cmwba = 1
    cmlaa = 2
