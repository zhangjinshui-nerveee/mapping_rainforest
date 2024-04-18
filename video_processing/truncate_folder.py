import os
import shutil

if __name__ == "__main__":
    workdir = "P0740368"
    outdir = f"{workdir}_trunc/"
    counter = 1
    os.makedirs(os.path.dirname(outdir), exist_ok=True)
    for root, dirs, filenames in os.walk(workdir):
        for fileName in filenames:
            frameNum = int(fileName[5:10])
            if frameNum % 24 == 0:
                shutil.copy2(workdir+"/"+fileName,outdir)

            counter += 1
        break # do not recurse into directories
