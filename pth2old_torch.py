# here to transfer .pth file so that it can be loaded in torch in old version
# use {{new version}}!!!!! pytorch to load!!

import torch


def transfer(filename, new_name):
    file = torch.load(filename)
    torch.save(file, new_name, _use_new_zipfile_serialization=False)


if __name__ == "__main__":
    transfer('checkpoint/RRDB_PSNR_x4.pth', 'checkpoint/RRDB_PSNR_x4_old.pth')
