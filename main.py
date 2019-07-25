# -*- coding: utf-8 -*-
from __future__ import division
from os import listdir, path, system, makedirs, remove
from shutil import rmtree
import cv2


def main():
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
        if file_count % 10 == 0:
            print(_file)
        input_file = path.join(in_path, _file)
        if path.isfile(input_file):
            if _file.split(".")[-1].lower() != "ppm":
                # convert to ppm
                system(path.join(external_path, "convert.exe" + " " + input_file
                                 + " " + path.join(tmp_path, _file.split(".")[0] + ".ppm")))
            src_image = cv2.imread(input_file, -1)
            # apply MLAA
            system(path.join(external_path, "mlaa.exe" + " " + path.join(tmp_path, _file.split(".")[0] + ".ppm")
                             + " " + path.join(tmp_path, _file.split(".")[0] + "_AA.ppm")))
            # delete temp ppm file
            remove(path.join(tmp_path, _file.split(".")[0] + ".ppm"))
            # convert to png
            save_file = path.join(out_path, _file.split(".")[0] + ".png")
            system(path.join(external_path, "convert.exe" + " " + path.join(tmp_path, _file.split(".")[0] + "_AA.ppm")
                             + " " + save_file))
            dst_image = cv2.imread(save_file, -1)
            if src_image.shape != dst_image.shape:
                h, w = src_image.shape
                image_resize = cv2.resize(dst_image, (w, h), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(save_file, image_resize)
            # delete temp AA ppm file
            remove(path.join(tmp_path, _file.split(".")[0] + "_AA.ppm"))

            file_count += 1


if __name__ == '__main__':
    main()
