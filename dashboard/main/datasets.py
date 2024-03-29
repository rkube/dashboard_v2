# -*- Encoding: UTF-8 -*-


from pymongo import MongoClient
import gridfs
import pickle
import torch
from torch.utils.data import Dataset



class ECEIDataset(Dataset):
    """ECEI Magnetic Island dataset."""

    def __init__(self, shotnr, coll_name, time_chunk_idx, return_mask=True):
        """ 
        Args:
            shotnr (int): KSTAR shot number
            coll_name (string): MongoDB collection name containing image data and masks
            return_mask (bool): If True return labelled mask with the frame
        """
        self.shotnr = shotnr
        self.return_mask = return_mask

        with open("mongo_uri", "r") as df:
            mongo_uri = df.readline().strip()

        with open("mongo_pass", "r") as df:
            mongo_pass = df.readline().strip()

        with open("mongo_user", "r") as df:
            mongo_user = df.readline().strip()

        mc = MongoClient(mongo_uri, username=mongo_user, password=mongo_pass, directConnection=True)
        db = mc.get_database()
        gfs = gridfs.GridFS(db)
        coll_pre = db.get_collection(coll_name)

        # Load a chunk with 10_000 frames
        frames, rarr, zarr = self._cache_frames(coll_pre, gfs, time_chunk_idx)
        self.frames = frames.reshape((24, 8, 10000))
        self.rarr = rarr.reshape((24, 8)) 
        self.zarr = zarr.reshape((24, 8)) 

        # Find all instances of image masks
        self.mask_list = []
        for post in coll_pre.find({"mask": {"$exists": True}}):
            self.mask_list.append({"frame_idx": post["frame_idx"], "mask": torch.tensor(post["mask"]).reshape(24, 8)})

    def __len__(self):
        if self.return_mask:
            return len(self.mask_list)
        return self.frames.shape[-1]

    def _cache_frames(self, coll_pre, gfs, chunk_idx):
        """Load chunk of ECEI data from MongoDB."""
        post = coll_pre.find_one({"description": "analysis results", "chunk_idx": chunk_idx})
        gridfs_handle = gfs.get(post["result_gridfs"])
        data_gfs = gridfs_handle.read()
        chunk_norm = pickle.loads(data_gfs)
        chunk_norm = (chunk_norm - chunk_norm.mean(axis=1, keepdims=True)) / (chunk_norm.std(axis=1, keepdims=True) + 1e-8)

        # Extract meta-data
        chunk_meta = coll_pre.find_one({"description": "metadata", "chunk_idx": chunk_idx})
        rarr = torch.tensor(chunk_meta["rarr"]).reshape(24, 8)
        zarr = torch.tensor(chunk_meta["zarr"]).reshape(24, 8)

        return chunk_norm, rarr, zarr

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        if self.return_mask:
            frameidx = self.mask_list[idx]["frame_idx"]
            mask = self.mask_list[idx]["mask"]  
        else:
            frameidx = idx 
            mask = torch.tensor([])

        frame = torch.tensor(self.frames[:, :, frameidx], dtype=torch.float32)
        frame.unsqueeze_(0)

        # Fix NaNs
        frame[torch.isnan(frame)] = 0.0

        return frame, mask