from ffmpeg_quality_metrics import FfmpegQualityMetrics as ffqm
# from cleanfid import fid
import lpips
import os
from skimage import img_as_float32
from imageio import mimread
import numpy as np
import torch
import sys


##############################################################################
# perpare state
# find path, create function
##############################################################################
print("\n\t#################################################")
print("\t#            Enter Prepare state                #")
print("\t#################################################")

# useful tool
def read_video(path):
    video = np.array(mimread(path))  # (24, 256, 256, 3)
    video_array = img_as_float32(video)
    video_array = torch.from_numpy(video_array)
    video_array.cuda()
    return video_array


# get the generated results, both in img/vid
path_to_gen = "reconstruction"
path_to_gen_vid = os.path.join(path_to_gen, "vids")
path_to_gen_img = os.path.join(path_to_gen, "imgs")
print("\t->[find] path to ground truth completed")

# get the ground truth results, both in img/vid
path_to_gt = "FaceForensics++/test/"
path_to_gt_vid = os.path.join(path_to_gt, "vid")
path_to_gt_img = os.path.join(path_to_gt, "img")
print("\t->[find] path to generated result completed")

# get the item list form generated folder, both img/vid
gen_videos = sorted(os.listdir(path_to_gen_vid))
gen_imgs = sorted(os.listdir(path_to_gen_img))
print("\t->[get] ground truth item(img_folder/vid) form path")

# get the item list form ground truth folder, both img/vid
gt_videos = sorted(os.listdir(path_to_gt_vid))
gt_imgs = sorted(os.listdir(path_to_gt_img))
print("\t->[get] generated result item(img_folder/vid) form path")

# simply check if the data match each other
dataset_len = len(gen_videos)
assert len(gt_videos) == len(gen_videos), "ref video failed to matching dist video"
print("\t->[check] data match each other")


# define funciton
lpips_fn = lpips.LPIPS(net="alex")
CriterionL2 = torch.nn.MSELoss().cuda()
CriterionL1 = torch.nn.L1Loss().cuda()

print("\t->[finish] all clear!")
print("\n\t#################################################")
print("\t#              Enter Metric state               #")
print("\t#################################################")

# init dic
score = {}
score["l1"] = 0
score["ssim"] = 0
score["psnr"] = 0
# score["fid"] = 0
score["lpips"] = 0


# confirm
print("\tthe metrics are following(%d):" % len(score))
for key, _ in score.items():
    print("\t->", key)
answer = input("\trun metrics?([y]/n)")

if answer != "y" and answer != "":
    sys.exit()

print("\n\t#################################################")
print("\t#            Metric start! Good Luck!           #")
print("\t#################################################")

# into metrice loop
for index in range(dataset_len):
    print("\n\t### now mesaure %s... ###" % gt_videos[index])

    # point path to the specific groud truth dataset, both vid/img
    gt_path_vid = os.path.join(path_to_gt_vid, gt_videos[index])
    gt_path_img = os.path.join(path_to_gt_img, gt_imgs[index])
    # point path to the specific generated rusult, both vid/img
    gen_path_vid = os.path.join(path_to_gen_vid, gen_videos[index])
    gen_path_img = os.path.join(path_to_gen_img, gen_imgs[index])

    #####################
    # SSIM & PSNR       #
    #####################
    a = ffqm(gt_path_vid, gen_path_vid)
    a.calc(["ssim", "psnr"])
    dic = a.get_global_stats()
    score["psnr"] += dic["psnr"]["average"]
    score["ssim"] += dic["ssim"]["average"]
    print("\t-> [SSIM] finish ")
    print("\t-> [PSNR] finish ")

    #####################
    # L1        		#
    #####################
    gen_array = read_video(gen_path_vid).unsqueeze(0)
    gt_array = read_video(gt_path_vid).unsqueeze(0)
    score["l1"] += CriterionL1(gen_array, gt_array).numpy()
    print("\t-> [L1] finish ")

    #####################
    # FID				#
    #####################
    # score["fid"] += fid.compute_fid(gt_path_img, gen_path_img)
    # print("\t-> [FID] finish ")

    #####################
    # LPIPS				#
    #####################
    score_ = 0
    for path1, path2 in zip(os.listdir(gt_path_img), os.listdir(gen_path_img)):
        # Load images
        gt_img = lpips.im2tensor(
            lpips.load_image(os.path.join(gt_path_img, path1))
        )  # RGB image from [-1,1]
        gen_img = lpips.im2tensor(lpips.load_image(os.path.join(gen_path_img, path2)))
        d = lpips_fn.forward(gt_img, gen_img)
        score_ += d.item()
    score["lpips"] += score_ / len(os.listdir(gt_path_img))
    print("\t-> [LPIPS] finish ")


for key, item in score.items():
    if key != "akd":
        score[key] = round(item / dataset_len, 5)

##############################################################################
# end state
##############################################################################
print("\n\t#################################################")
print("\t#              Metric finished                  #")
print("\t#################################################")


print(score)

with open(os.path.join(path_to_gen, "results.txt"), "w") as f:
    f.write(str(score))
