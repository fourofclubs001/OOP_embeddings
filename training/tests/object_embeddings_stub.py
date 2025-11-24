import torch
import torch.nn as nn

class ObjectEmbedding(nn.Module):
    def __init__(self, 
                 embedding_dim, 
                 colabs_int_size,
                 colabs_ext_size, 
                 output_size):
        super(ObjectEmbedding, self).__init__()
        self.params = nn.Linear(embedding_dim, colabs_int_size)
        self.embedding_size = embedding_dim
    def forward(self, 
                class_method,   # embedding <clase,metodo>
                recep_obj,      # embedding objeto receptor
                int_colabs,     # lista de embeddings de colaboradores internos 
                ext_colabs,     # lista de embeddings de colaboradores externos 
                ):
        return torch.zeros(1,self.embedding_size)