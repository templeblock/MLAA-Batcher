from os import listdir, path, system, makedirs, remove
from shutil import rmtree

in_path = "in"
tmp_path = "tmp"
out_path = "out"
external_path = "external"

try:
	rmtree(tmp_path)
except:
	pass
makedirs(tmp_path, exist_ok=True)

file_count = 0

for _file in listdir(in_path):
	if file_count%10 == 0:
		print(_file)
	if path.isfile(path.join(in_path, _file)):
		if _file.split(".")[-1].lower() != "ppm":
			# convert to ppm
			system(path.join(external_path, "convert.exe" + " " + path.join(in_path, _file)
							 + " " + path.join(tmp_path, _file.split(".")[0] + ".ppm")))

		# apply MLAA
		system(path.join(external_path, "mlaa.exe" + " " + path.join(tmp_path, _file.split(".")[0] + ".ppm")
						 + " " + path.join(tmp_path, _file.split(".")[0] + "_AA.ppm")))

		# delete temp ppm file
		remove(path.join(tmp_path, _file.split(".")[0] + ".ppm"))

		# convert to png
		system(path.join(external_path, "convert.exe" + " " + path.join(tmp_path, _file.split(".")[0] + "_AA.ppm")
						 + " " + path.join(out_path, _file.split(".")[0] + ".png")))

		# delete temp AA ppm file
		remove(path.join(tmp_path, _file.split(".")[0] + "_AA.ppm"))

		file_count += 1




