from torch.utils.data import Dataset
import numpy as np
import torch

# go through
class TrainDataset(Dataset):
    def __init__(self, df):
        self.user_ids = df['userId'].values
        self.movie_ids = df['movieId'].values
        self.ratings = df['rating'].values
    
    def __len__(self):
        return len(self.user_ids)
    
    def __getitem__(self, idx):
        user = self.user_ids[idx]
        item = self.movie_ids[idx]
        rating = self.ratings[idx]
        return (user, item, rating)

# computes random triplets of user id, positive movie, negative movie
class TrainDatasetBPR(Dataset):
    def __init__(self, file, num_users, num_movies):
        self.file = file
        self.num_users = num_users
        self.num_movies = num_movies

    def __len__(self):
        return len(self.file)

    def __getitem__(self, idx):
        return self.pick_random()

    def pick_random(self):
        # pick random movie
        user =  np.random.randint(0, self.num_users)
        # store all the positive movies
        filtered_movies = self.file[(self.file['userId'] == user) & (self.file['rating'] > 0.5)]
        movie_ids = filtered_movies['movieId'].tolist()
        # pick random positive movie
        if len(movie_ids) == 0:
            return self.pick_random()
        pos_index =  np.random.randint(0, len(movie_ids))
        pos_movie = movie_ids[pos_index]
        # pick random neg movie
        neg_index = np.random.randint(0, self.num_movies)
        neg_index = self.get_negative(neg_index, movie_ids)
        neg_movie = neg_index
        return (torch.tensor(user, dtype=torch.long),
                torch.tensor(pos_movie, dtype=torch.long),
                torch.tensor(neg_movie, dtype=torch.long))
    
    def get_negative(self, neg_index, positive_movies):
        while neg_index in positive_movies:
            neg_index = np.random.randint(0, self.num_movies)
        return neg_index