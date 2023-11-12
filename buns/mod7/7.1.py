import cProfile
from functions_to_profile import load_files, read_database, get_id, get_user_data, generate_words
import pstats

TASK_FUNCTIONS_ORDER = ['load_files', 'read_database', 'get_id', 'get_user_data', 'generate_words']

profile = cProfile.Profile()
profile.enable()
for i in TASK_FUNCTIONS_ORDER:
	if i == "load_files":
		load_files()
	elif i == "read_database":
		read_database()
	elif i == "get_id":
		get_id()
	elif i == "get_user_data":
		get_user_data()
	elif i == "generate_words":
		generate_words()
profile.disable()
profile.create_stats()

p = pstats.Stats(profile)
p = p.get_stats_profile()

for i in TASK_FUNCTIONS_ORDER:
    print(f"{p.func_profiles[i].cumtime:.4f}: {int(p.func_profiles[i].cumtime/p.total_tt*100)}%")