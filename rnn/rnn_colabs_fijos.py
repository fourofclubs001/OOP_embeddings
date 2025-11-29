import torch
import torch.nn as nn

class ObjectEmbedding(nn.Module):
    def __init__(self, 
                 embedding_dim, 
                 colabs_int_size,
                 colabs_ext_size, 
                 output_size):
        super(ObjectEmbedding, self).__init__()

        #Cálculo input size
        #La entrada es la suma de:
        #1. Embedding <clase,método> --> embedding_dim
        #2. Embedding objeto receptor --> embedding_dim
        #3. Lista de embeddings de colabs internos --> n vectores
        #3. Lista de embeddings de colabs externos --> m vectores

        self.final_input_size = embedding_dim * (2 + colabs_ext_size + colabs_int_size)
        
        #Feed-Forward Multicapa
        self.final_rnn = nn.Sequential(
            nn.Linear(self.final_input_size, self.final_input_size // 2),
            nn.ReLU(),
            nn.Linear(self.final_input_size // 2, output_size)
        )

    def forward(self, 
                class_method,   # embedding <clase,metodo>
                recep_obj,      # embedding objeto receptor
                int_colabs,     # lista de embeddings de colaboradores internos 
                ext_colabs,     # lista de embeddings de colaboradores externos 
                ):
        
        # 1. Obtener el tamaño del batch
        batch_size = class_method.size(0)

        # 2. Aplanar (Flatten) los colaboradores
        # Transformamos de (Batch, N, Dim) a (Batch, N * Dim)
        # El -1 es para que PyTorch calcule la dimensión restante
        int_colabs_flat = int_colabs.reshape(batch_size, -1)
        ext_colabs_flat = ext_colabs.reshape(batch_size, -1)
        
        # 3. Concatenamos todo en un solo vector
        combined_vector = torch.cat([
            class_method,
            recep_obj,
            int_colabs_flat,
            ext_colabs_flat
        ], dim=1) 
        
        # 4. Pasar por la Feed-Forward
        final_output = self.final_rnn(combined_vector)
        
        return final_output
