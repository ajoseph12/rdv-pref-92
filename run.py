from rdv_pref_94 import RDVPREF94
import time

#run script
if __name__ == '__main__':
	print("Sleeping for 5 minutes...")
	time.sleep(300)

	r = RDVPREF94()
	r.loop_rdv_find_executor()
